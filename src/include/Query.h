#ifndef SRC_PYDGGRID_QUERY_H
#define SRC_PYDGGRID_QUERY_H
#include <string>
#include <vector>
#include <map>
#include <cstdio>
#include <sstream>
#include <filesystem>
#include "Functions.h"
#include "Constants.h"
#include "Bytes.h"
#include "../pydggrid/OpBasic.h"
#include "../pydggrid/SubOpStats.h"
#include <dglib/DgOWStream.h>

namespace pydggrid
{
    class Query
    {
        public:

            /**
             * Default constructor
             * @param parameterData Parameter Data
             * @param byteData Bytes Data
             */
            Query(const std::map<std::string, std::string> &parameterData,
                  const std::vector<unsigned char> &byteData)
            {
                for (const auto& parameter : parameterData)
                    { this->parameters[parameter.first] = std::string{parameter.second}; }
                this->parameters["verbosity"] = "0";
                //
                this->bin.clear();
                this->bin.resize(0);
                this->readBytes(byteData);
                this->writeBinaries();
                this->writeRegisters();
                this->writeOutputs();
                this->operation = std::make_unique<OpBasic>(this->parameters);
                //
                this->copyStreams();
            };

            /**
             * Query deconstructor
             */
            ~Query()
            {
                this->close();
            }

            /**
             * Runs the query
             * @return Query Object
             */
            Query *run()
            {
                this->operation->initialize();
                this->operation->execute();
                this->response["meta"] = this->metaBin();
                this->response["cells"] = this->operation->outOp.getCells();
                this->response["points"] = this->operation->outOp.getPoints();
                this->response["collection"] = this->operation->outOp.getCollection();
                this->response["pr_cells"] = this->operation->outOp.getPRCells();
                this->response["r_points"] = this->operation->outOp.getRPoints();
                this->response["collection"] = this->operation->outOp.getCollection();
                this->response["statistics"] = this->statisticBlocks();
                this->response["dataset"] = this->operation->outOp.getDataOut();
                if (this->isPointQuery())
                    { this->response["dataset"] = this->operation->outOp.getTextOut(); }
                this->operation->cleanup();
                if (this->isOutFile("cell"))
                    { this->response["cells"] = this->getData("cell"); }
                if (this->isOutFile("point"))
                    { this->response["points"] = this->getData("point"); }
                if (this->isOutFile("collection"))
                    { this->response["collection"] = this->getData("collection"); }
                //
                return this;
            };

            /**
             * Closes the query
             * @return
             */
            Query *close()
            {
                for (const std::string &filename : this->IOGC)
                {
                    std::remove(filename.c_str());
                }
                this->IOGC.clear();
                this->operation->cleanup();
                return this;
            }

            /**
             * Returns number of inputs available for processing or clip
             * @return Input Size
             */
            size_t getInputSize()
            {
                return this->binSize;
            }

            /**
             * Gets response data by name
             * @param responseCode Response Code
             * @return Response Code Bytes
             */
            std::vector<unsigned char> getResponse(const char *responseCode)
            {
                return (this->response.find(responseCode) == this->response.end()) ?
                    std::vector<unsigned char>{} : std::vector<unsigned char>{this->response[responseCode]};
            }

            /**
             * Returns response bytes of the query
             * @return Response Bytes
             */
            std::vector<unsigned char> toBytes()
            {
                std::vector<unsigned char> elements;
                for (const std::string &responseName : Constants::response_indexes)
                {
                    if (this->response.find(responseName) != this->response.end())
                    {
                        elements.emplace_back(this->response[responseName].size());
                        elements.insert(elements.end(),
                                        this->response[responseName].begin(),
                                        this->response[responseName].end());
                    }
                }
                return elements;
            }

            /**
             * Writes the dggrid query to response object
             * @return Query As String
             */
            std::string toString()
            {
                std::stringstream stream;
                stream << "PARAMETERS: " << std::endl;
                for (const auto &parameter : this->parameters)
                    { stream << "\t" << parameter.first << " = " << parameter.second << std::endl; }
                stream << "PAYLOAD:" << std::endl;
                stream << "\t" << this->getInputSize() << " packets";
                for (size_t index = 0; index < this->getInputSize(); index++)
                {
                    stream << "[" << (index + 1) << "] ";
                    stream << this->DataTypeLabel(this->bin_t[index]) << std::endl;
                    stream << "\t" << Functions::wrapString(this->dataString(index),
                                                            256,
                                                            "\n\t");
                    stream << std::endl;
                }
                stream << "RESPONSE:" << std::endl;
                for (const auto &responseData : this->response)
                {
                    stream << "\t" << responseData.first << " (";
                    stream << responseData.second.size() << " b.)" << std::endl;
                    stream << "\t" << Functions::wrapString(Functions::to_hex(responseData.second),
                                                            256,
                                                            "\n\t");
                    stream << std::endl;
                    stream << std::endl;
                }
                return {stream.str()};
            }

            /**
             * Returns packet data type integer
             * @param index Packet Index
             * @return DataType index
             */
            int getDataType(size_t index)
            {
                return (index < this->binSize) ? this->bin_t[index] : -1;
            }

            /**
             * Gets packet size of specific payload bin
             * @param index Payload index
             * @return Size of byte payload
             */
            size_t getPacketSize(size_t index)
            {
                return (index < this->binSize) ? this->bin[index].size() : -1;
            }

        private:
            size_t binSize = 0;
            std::vector<int>  bin_t;
            std::vector<std::vector<unsigned char> >  bin;
            std::map<std::string, std::string> parameters;
            std::map<std::string, std::vector<unsigned char> > response;
            //
            std::unique_ptr<OpBasic> operation;
            std::vector<std::string> REGF; // region registration set
            std::vector<std::string> IOGC; // I/o garbage collection
            std::map<std::string, std::vector<std::string> > streams;

            /**
             * Returns the meta response data as a byte array
             * @return  Meta Data vector
             */
            std::vector<unsigned char> metaBin()
            {
                std::vector<unsigned char> elements;
                elements.insert(elements.begin(),
                                this->operation->metaResponse.begin(),
                                this->operation->metaResponse.end());
                return elements;
            }

            /**
             * Returns data type label
             * @param dataType Data Type Integer
             * @return Data Type Label String
             */
            std::string DataTypeLabel(int dataType)
            {
                // TODO | Make this a static map
                if (dataType == Constants::DataTypes::INT) { return "INT"; }
                if (dataType == Constants::DataTypes::FLOAT) { return "FLOAT"; }
                if (dataType == Constants::DataTypes::SHORT) { return "SHORT"; }
                if (dataType == Constants::DataTypes::BINARY) { return "BINARY"; }
                if (dataType == Constants::DataTypes::STRING) { return "STRING"; }
                if (dataType == Constants::DataTypes::SHAPE_BINARY) { return "SHAPE_BINARY"; }
                if (dataType == Constants::DataTypes::LOCATION) { return "LOCATION"; }
                return "UNKNOWN";
            }

            /**
             * Returns a string representation of payload data
             * @param index Data Index
             * @return Data String
             */
            std::string dataString(size_t index)
            {
                if ((this->bin_t[index] == Constants::DataTypes::BINARY) ||
                    (this->bin_t[index] == Constants::DataTypes::SHAPE_BINARY) ||
                    (this->bin_t[index] == Constants::DataTypes::LOCATION))
                {
                    return Functions::to_hex(this->bin[index]);
                }

                return "";
            }

            /**
             * Reads bytes into the query object
             * @param byteData Byte Data from python
             */
            void readBytes(const std::vector<unsigned char> &byteData)
            {
                Bytes bytes(byteData);
                if (!bytes.isEmpty())
                {
                    this->binSize = bytes.getInt();
                    for (int index = 0; index < this->binSize; index++)
                    {
                        this->bin_t.emplace_back(bytes.getInt());
                        this->bin.emplace_back(bytes.getBytes());
                    }
                }
            }

            /**
             * Writes binary files if any exist in the buffer
             */
            void writeBinaries()
            {
                size_t input_size = this->getInputSize();
                for (size_t index = 0; index < input_size; index++)
                {
                    // Write shape file
                    if ((this->getDataType(index) == Constants::DataTypes::SHAPE_BINARY))
                    {
                        Bytes bytes(this->bin[index]);
                        char filename[] = "/tmp/PYDGGRID.XXXXXX"; // template for our file.
                        int fd = mkstemp(filename);
                        std::string base = std::string(filename);
                        int element_size = bytes.getInt();
                        for (size_t element_index = 0; element_index < element_size; element_index++)
                        {
                            std::string file_extension = bytes.getString();
                            std::vector<unsigned char> file_data = bytes.getBytes();
                            std::string file_name = base + std::string(".") + file_extension;
                            Functions::writeBinary(file_name.c_str(),
                                                   file_data.data(),
                                                   file_data.size());
                            if (file_extension == "shp") { this->REGF.emplace_back(file_name); }
                            this->IOGC.emplace_back(file_name);
                        }
                    }
                    if ((this->getDataType(index) == Constants::DataTypes::INT))
                    {
                        Bytes bytes(this->bin[index]);
                        size_t blockSize = bytes.getInt();
                        std::vector<std::string> elements;
                        elements.resize(blockSize);
                        for (size_t block = 0; block < blockSize; block++)
                            { elements[block] = std::to_string(bytes.getInt()); }
                        std::string enumID = "INT-" + std::to_string((index + 1));
                        this->streams.insert({enumID, std::vector<std::string>{elements}});
                        this->REGF.emplace_back(enumID);
                    }
                    if ((this->getDataType(index) == Constants::DataTypes::STRING))
                    {
                        Bytes bytes(this->bin[index]);
                        if (!this->isGdal())
                        {
                            std::vector<std::string> elements = Functions::split(bytes.getString(), "\n");
                            std::string enumID = "STR-" + std::to_string((index + 1));
                            this->streams.insert({enumID, std::vector<std::string>{elements}});
                            this->REGF.emplace_back(enumID);
                        }
                        else
                        {
                            std::string fileName = this->tmpFile();
                            std::vector<unsigned char> fileData = bytes.getBytes();
                            Functions::writeBinary(fileName.c_str(),
                                                   fileData.data(),
                                                   fileData.size());
                            this->REGF.emplace_back(fileName);
                        }
                    }
                    if (this->getDataType(index) == Constants::DataTypes::LOCATION)
                    {
                        std::vector<std::string> elements;
                        Bytes bytes(this->bin[index]);
                        auto recordSize = (size_t) bytes.getInt();
                        for (size_t recordIndex = 0; recordIndex < recordSize; recordIndex++)
                        {
                            std::stringstream stream;
                            stream << bytes.getFloat() << "|";
                            stream << bytes.getFloat() << "|";
                            stream << bytes.getInt() << "|";
                            stream << bytes.getString();
                            elements.emplace_back(stream.str());
                        }
                        std::string enumID = "STR-" + std::to_string((index + 1));
                        this->streams.insert({enumID, std::vector<std::string>{elements}});
                        this->REGF.emplace_back(enumID);
                    }
                }
            }

            /**
             * Write register files from tmpfs
             */
            void writeRegisters()
            {
                //** Region File registrations **/
                if (!this->REGF.empty())
                {
                    std::ostringstream region_files;
                    std::copy(this->REGF.begin(),
                              this->REGF.end(),
                              std::ostream_iterator<std::string>(region_files, " "));
                    if (this->isGenerateQuery())
                    {
                        this->parameters["clip_region_files"] = region_files.str();
                    }
                    if (this->isPointQuery())
                    {
                        this->parameters["input_files"] = region_files.str();
                    }
                    if (this->isTransformQuery())
                    {
                        this->parameters["input_file_name"] = region_files.str();
                    }
                    this->REGF.clear();
                    this->REGF.resize(0);
                }
            }

            /**
             * Writes output handlers, usually used to catch the output of GDAL files
             */
            void writeOutputs()
            {
                if (!this->isOutFile()) { return; }
                for (auto &data_index : Constants::data_indexes)
                {
                    if (!this->getGDALType(data_index.c_str()).empty())
                    {
                        this->setOutputFile(data_index.c_str());
                    }
                    else if (this->getOutputType(data_index.c_str()) == "SHAPEFILE")
                    {
                        this->setOutputFile(data_index.c_str());
                    }
                }
            }

            /**
             * Returns true if the system uses an outfile
             * @return True if an outfile is used
             */
            bool isOutFile()
            {
                for (const std::string &data_index : Constants::data_indexes)
                {
                    if (this->isOutFile(data_index.c_str())) { return true; }
                }
                return false;
            }

            /**
             * Returns true if the given vector id is an outfile
             * @param dataIndex  Data Index
             * @return True if outfile
             */
            bool isOutFile(const char* dataIndex)
            {
                return  ((!this->getGDALType(dataIndex).empty()) ||
                        (this->getOutputType(dataIndex) == "SHAPEFILE"));
            }

            /**
             * Returns true if the query is of grid generation type
             * @return True if GENERATE_GRID
             */
            bool isGenerateQuery()
            {
                if (this->parameters.find("dggrid_operation")->second == "GENERATE_GRID") { return true; }
                return false;
            }

            /**
             * Returns true if the query is of point presence or point value type
             * @return True if BIN_POINT_PRESENCE or BIN_POINT_VALS
             */
            bool isPointQuery()
            {
                if (this->parameters.find("dggrid_operation")->second == "BIN_POINT_PRESENCE") { return true; }
                if (this->parameters.find("dggrid_operation")->second == "BIN_POINT_VALS") { return true; }
                if (this->parameters.find("dggrid_operation")->second == "GENERATE_GRID_FROM_POINTS") { return true; }
                return false;
            }

            /**
             * Returns true if the query is of point presence or point value type
             * @return True if BIN_POINT_PRESENCE or BIN_POINT_VALS
             */
            bool isTransformQuery()
            {
                return (this->parameters.find("dggrid_operation")->second == "TRANSFORM_POINTS");
            }

            /**
             * Returns true if the query carries a GDAL package
             * @return True if GDAL
             */
            bool isGdal()
            {
                if (this->isPointQuery())
                {
                    return (this->parameters.find("point_input_file_type") != this->parameters.end()) &&
                           (this->parameters.find("point_input_file_type")->second == "GDAL");
                }
                if ((this->parameters.find("clip_subset_type") != this->parameters.end()) &&
                    (this->parameters["clip_subset_type"] == "GDAL")) { return  true; }
                return false;
            }

            /**
             * Copies stream data to opBasic
             */
            void copyStreams()
            {
                //** Region File registrations **/
                for (auto const &streamNode : this->streams)
                {
                    this->operation->stringStreamData.insert({streamNode.first, streamNode.second});
                }
            }

            /**
             * Creates a temp file with extension and returns name
             * @param extension Extension String
             * @return Temp File Name
             */
            std::string tmpFile()
            {
                char filename[] = "/tmp/PYDGGRID.XXXXXX"; // template for our file.
                int _ = mkstemp(filename);
                std::string fileName{filename};
                std::remove(fileName.c_str());
                return fileName;
            }

            /**
             * Gets output file data by vector id
             * @param vectorID Vector ID ie. "collection"
             * @return Response Byte Vector
             */
            std::vector<unsigned char> getData(const std::string& vectorID)
            {
                std::string field_f = Functions::string_format("%s_output_gdal_format", vectorID.c_str());
                std::string file_f = Functions::string_format("%s_output_file_name", vectorID.c_str());
                if (this->parameters.find(field_f) != this->parameters.end())
                {
                    return Functions::readBinary(this->parameters[file_f].c_str());
                }
                //
                field_f = Functions::string_format("%s_output_type", vectorID.c_str());
                if (this->parameters.find(field_f) != this->parameters.end())
                {
                    if (this->parameters[field_f] == "SHAPEFILE")
                    {
                        return this->shapeData(this->parameters[file_f].c_str());
                    }
                }
                return {};
            }

            /**
             * Returns a shape data array
             * @param fileName File Name
             * @return Condensed shape data
             */
            std::vector<unsigned char> shapeData(const char *fileName)
            {
                std::vector<unsigned char> bytes;
                for (const auto &extension : Constants::shapefile_extensions)
                {
                    std::string f_name = Functions::string_format("%s.%s", fileName, extension.c_str());
                    std::vector<unsigned char> byteData = Functions::readBinary(f_name.c_str());
                    std::vector<unsigned char> byteSize = Functions::to_bytes(byteData.size());
                    bytes.insert(bytes.end(), extension.begin(), extension.end());
                    bytes.insert(bytes.end(), byteSize.begin(), byteSize.end());
                    bytes.insert(bytes.end(), byteData.begin(), byteData.end());
                }
                return {bytes};
            };

            /**
             * returns output type based on data index
             * @param dataIndex Data Index
             * @return Output Type String
             */
            std::string getOutputType(const char *dataIndex)
            {
                std::string type_f = "%s_output_type";
                std::string field_f = Functions::string_format(type_f, dataIndex);
                return (this->parameters.find(field_f) != this->parameters.end()) ?
                    this->parameters[field_f] : "";
            };

            /**
             * returns output type based on data index
             * @param dataIndex Data Index
             * @return Output Type String
             */
            std::string getGDALType(const char *dataIndex)
            {
                std::string field_f = Functions::string_format("%s_output_gdal_format", dataIndex);
                return (this->parameters.find(field_f) != this->parameters.end()) ?
                    this->parameters[field_f] : "";
            };

            /**
             * Sets the output file to temp directory
             * @param dataIndex Data Index
             */
            void setOutputFile(const char *dataIndex)
            {
                std::string file_f = Functions::string_format("%s_output_file_name", dataIndex);
                this->parameters[file_f] = this->tmpFile();
                this->IOGC.emplace_back(this->parameters[file_f]);
            }

            /**
             * Retrieves statistic blocks for object
             * @return Statistic blocks string
             */
            std::vector<unsigned char> statisticBlocks()
            {
                if (this->parameters.find("dggrid_operation")->second == "OUTPUT_STATS")
                {
                    std::vector<unsigned char> elements{};
                    size_t statisticSize = this->operation->statisticBlocks.size();
                    for (size_t statistic_index = 0; statistic_index < statisticSize; statistic_index++)
                    {
                        size_t cellSize = this->operation->statisticBlocks[statistic_index].size();
                        for (size_t cell_index = 0; cell_index < cellSize; cell_index++)
                        {
                            char end_character = (cell_index == (cellSize - 1)) ? '\n' : '|';
                            std::string statistic_value = this->operation->statisticBlocks[statistic_index][cell_index];
                            std::vector<unsigned char> statistic_element(statistic_value.data(),
                                                                         statistic_value.data() +
                                                                         statistic_value.length() + 1);

                            elements.insert(elements.end(),
                                            statistic_element.begin(),
                                            statistic_element.end());
                            elements.emplace_back((unsigned char) end_character);
                        }
                    }
                    return elements;
                }
                return std::vector<unsigned char>{};
            }
    };
}
#endif //SRC_PYDGGRID_QUERY_H