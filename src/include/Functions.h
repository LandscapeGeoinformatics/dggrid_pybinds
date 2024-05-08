#ifndef SRC_PYDGGRID_FUNCTIONS_H
#define SRC_PYDGGRID_FUNCTIONS_H
#include <any>
#include <memory>
#include <string>
#include <vector>
#include <climits>
#include <stdexcept>
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <iostream>
#include <filesystem>

namespace pydggrid::Functions
{
    /**
     * Formats String
     * @tparam Args  Formatting Type
     * @param format Format String
     * @param args Formatting Data
     * @return Formatted String
     */
    template<typename ... Args>
    static std::string string_format( const std::string& format, Args ... args )
    {
        int size_s = std::snprintf( nullptr, 0, format.c_str(), args ... ) + 1; // Extra space for '\0'
        if( size_s <= 0 ){ throw std::runtime_error( "Error during formatting." ); }
        auto size = static_cast<size_t>( size_s );
        std::unique_ptr<char[]> buf( new char[ size ] );
        std::snprintf( buf.get(), size, format.c_str(), args ... );
        return std::string{(buf.get())};
    }

    /**
     * Throws an error
     * @param error_string Error String
     */
    static void throw_error(const std::string& error_string)
    {
        throw std::runtime_error(error_string);
    }

    /**
     * Throws an error with formatting
     * @param format Format String
     * @param args Formatting Data
     * @return Formatted String
     */
    template<typename ... Arguments>
    static void throw_error(const std::string& format, Arguments ... args)
    {
        Functions::throw_error(Functions::string_format(format, std::forward<Arguments>(args)...));
    }

    /**
     * Checks if array contains search variable
     * @tparam T AnyType
     * @param array Array
     * @param search Search Parameter
     * @return True if array contains search parameter
     */
    template<class T>
    static bool contains(std::vector<T> array, T search)
    {
        return std::find(array.begin(), array.end(), search) != array.end();
    }

    /**
     * Returns the index or SIZE_MAX if non existent
     * @tparam T AnyType
     * @param array Array
     * @param search Search Parameter
     * @return value index or SIZE_MAX if not in array
     */
    template<class T>
    static size_t getIndex(std::vector<T> array, T search)
    {
        auto it = std::find(array.begin(), array.end(), search);
        return (it == array.end()) ? SIZE_MAX : it - array.begin();
    }

    /**
         * Performs simple word wrap function with given delimiter
         * @param sentence Sentence to word wrap
         * @param width Wrap width
         * @param delimiter Delimiter default is '\\n'
         * @return Wrapped string
         */
    static std::string wordWrap(const std::string& sentence, int width, const std::string& delimiter = "\n")
    {
        std::stringstream stream;
        size_t string_size = sentence.length();
        for (size_t index = 0; index < string_size; index++)
        {
            stream << sentence.c_str()[index];
            if ((index % width) == 0)
            {
                stream << delimiter;
            }
        }
        std::string response_string = stream.str();
        return response_string;
    }

    /**
     * prints the byte buffer data as hexadecimal
     * @param buffer Buffer Object
     */
    static std::string to_hex(std::vector<unsigned char> bytes)
    {
        std::stringstream stream;
        const size_t inBufferSize = bytes.size();
        for (size_t byteIndex = 0; byteIndex < inBufferSize; byteIndex++)
        { stream << std::hex << std::setw(2) << std::setfill('0') << (0xff & bytes[byteIndex]); }
        std::string response_string = stream.str();
        return response_string;
    }

    /**
     * Converts hex string to byte array
     * @param stringData Hex String data
     * @return Byte Array
     */
    static std::vector<unsigned char> from_hex(const char *stringData)
    {
        int counter = 0;
        std::stringstream stream;
        std::string hexString{stringData};
        std::transform(hexString.begin(), hexString.end(), hexString.begin(), ::toupper);
        size_t hexSize = hexString.length();
        for (size_t index = 0; index < hexSize; index++)
        {
            if (std::isspace(hexString.at(index))) { continue; }
            stream << hexString.at(index);
            counter++;
            if (counter == 2)
            {
                counter = 0;
                stream << " ";
            }
        }

        std::vector<unsigned char> bytes;
        std::istringstream hex_chars_stream(stream.str());
        //
        unsigned int c;
        while (hex_chars_stream >> std::hex >> c) { bytes.push_back(c); }
        return bytes;
    }

    /**
     * Reads string content from a file
     * @param fileName File Name to read
     * @return File Contents as String
     */
    static std::string readString(const char *fileName)
    {
        std::string item_name;
        std::ifstream nameFileout;
        std::stringstream stream;
        nameFileout.open(fileName);
        //
        std::string line;
        while(std::getline(nameFileout, line)) { stream << line; }
        return {stream.str()};
    }

    /**
     * Simply wraps a string with a delimiter, not a word wrap function
     * @param string String to wrap
     * @param width String width
     * @param delimiter Delimiter
     * @return Wrapped String
     */
    static std::string
    wrapString(const std::string& string, int width, const char *delimiter = "\n")
    {
        std::stringstream  stream;
        size_t stringSize = string.size();
        for (size_t index = 0; index < stringSize; index++)
        {
            std::string insertChar = (((index % width) == 0) && (index > 0)) ? delimiter : "";
            stream << string.at(index) << insertChar;
        }
        return {stream.str()};
    }

    /**
     * Writes out a binary file
     * @param pathString Path String
     * @param byteData Byte Data
     * @param byteSize Byte Size
     */
    static void writeBinary(const char *pathString, unsigned char *byteData, size_t byteSize)
    {
        std::ofstream stream(pathString, std::ios::out | std::ios::binary | std::ios::app);
        stream.write((char *) byteData, (long) byteSize);
        stream.close();
    }

    /**
     * Reads a file into binary data
     * @param filename File Name
     * @return Binary File
     */
    static std::vector<unsigned char> readBinary(const char* filename)
    {
        try
        {
            char b;
            std::vector<unsigned char> elements;
            std::ifstream in(filename, std::ios::binary);
            if(in.is_open())
            {
                while(in.good())
                {
                    in.read(&b, 1);
                    elements.emplace_back(b);
                }
            }
            in.close();
            return {elements};
        }
        catch (...) { return {}; }
    }

    /**
     * Splits a string
     * @param s String data
     * @param delimiter Delimiter
     * @return String Blocks
     */
    static std::vector<std::string> split(std::string s, std::string delimiter)
    {
        size_t pos_start = 0, pos_end, delim_len = delimiter.length();
        std::string token;
        std::vector<std::string> res;

        while ((pos_end = s.find(delimiter, pos_start)) != std::string::npos) {
            token = s.substr (pos_start, pos_end - pos_start);
            pos_start = pos_end + delim_len;
            res.push_back (token);
        }

        res.push_back (s.substr (pos_start));
        return res;
    }

    /**
     * Saves an integer value to byte buffer
     * @param value Integer Value
     * @return Byte Byffer Object
     */
    static std::vector<unsigned char> to_bytes(uint32_t value)
    {
        unsigned char byteData[4];
        std::vector<unsigned char> bytes;
        memset(byteData, 0, sizeof(byteData));
        memcpy(byteData, &value, 4);
        bytes.insert(bytes.end(), byteData, byteData + 4);
        return {bytes};
    }
}
#endif //SRC_PYDGGRID_FUNCTIONS_H
