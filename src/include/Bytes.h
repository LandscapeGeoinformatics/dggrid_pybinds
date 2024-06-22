#ifndef SRC_BYTEBUFFER_H
#define SRC_BYTEBUFFER_H
#include <utility>
#include <vector>
#include <string>
#include <cstring>
#include <algorithm>

namespace pydggrid
{
    class Bytes
    {
        public:
            const static int intSize = 4;
            const static int floatSize = 4;

            /**
             * Empty constructor
             */
            Bytes()
            {
                this->data.clear();
                this->data.resize(0);
                this->size = 0;
            }

            /**
             * Byte Array constructor
             * @param byteArray Byte Array
             * @param byteSize Byte Array Size
             */
            Bytes(unsigned char *byteArray, size_t byteSize)
            {
                this->read(byteArray, byteSize);
            };

            /**
             * Vector constructor
             * @param byteArray Byte Array Vector
             */
            explicit Bytes(const std::vector<unsigned char>& byteArray)
            {
                this->read(byteArray);
            };

            /**
             * Hex string constructor
             * @param hexString Hex String Constructor
             */
            explicit Bytes(const char *hexString)
            {
                this->read(Functions::from_hex(hexString));
            }

            /**
             * Rewinds the index
             * @return Bytes object
             */
            Bytes *rewind()
            {
                this->index = 0;
                return this;
            };

            /**
             * Reads from a byte array
             * @param byteArray Byte Array
             * @param byteSize Byte Size
             * @return Bytes Object
             */
            Bytes *read(unsigned char *byteArray, size_t byteSize)
            {
                this->data.clear();
                this->data.resize(byteSize);
                this->data.assign(byteArray, byteArray + byteSize);
                this->size = byteSize;
                return this;
            };

            /**
             * Reads from a byte vector
             * @param byteArray Byte Vector
             * @return Bytes Object
             */
            Bytes *read(const std::vector<unsigned char>& byteArray)
            {
                this->data.clear();
                this->size = byteArray.size();
                this->data.resize(this->size);
                this->data.assign(byteArray.begin(), byteArray.end());
                return this;
            };

            /**
             * Returns true if the bytes data is empty
             * @return True if empty
             */
            bool isEmpty()
            {
                return (this->getSize() <= 0);
            }

            /**
             * Returns the current index
             * @return Current Byte Index
             */
            size_t getIndex()
            {
                return this->index;
            };

            /**
             * Returns the byte array size
             * @return Byte Size
             */
            size_t getSize()
            {
                return this->size;
            };

            /**
             * Returns the integer at current index
             * @return Integer at current index
             */
            int getInt()
            {
                return this->getInt(this->index);
            };

            /**
             * Returns the integer at given index
             * @param byteIndex Byte Index
             * @return Integer at given index
             */
            int getInt(size_t byteIndex)
            {
                int value = 0;
                size_t yIndex = byteIndex + Bytes::intSize;
                memcpy(&value, this->slice(this->data,
                                        (int) byteIndex,
                                        (int) yIndex).data(),
                       Bytes::intSize);
                this->index += Bytes::intSize;
                return value;
            };

            /**
             * Returns the float at current index
             * @return Float at current index
             */
            float getFloat()
            {
                return this->getFloat(this->index);
            };

            /**
             * Returns the float at given index
             * @param byteIndex Byte Index
             * @return Float at given index
             */
            float getFloat(size_t byteIndex)
            {
                float value = 0.0f;
                size_t yIndex = byteIndex + Bytes::floatSize;
                memcpy(&value, this->slice(this->data,
                                        (int) byteIndex,
                                        (int) yIndex).data(),
                       Bytes::intSize);
                this->index += Bytes::intSize;
                return value;
            };

            /**
             * Returns the string at current index
             * @return String Data
             */
            std::string getString()
            {
                return this->getString(this->getIndex());
            };

            /**
             * Returns the string at given index
             * @param byteIndex Byte Index
             * @return String Data
             */
            std::string getString(size_t byteIndex)
            {
                int stringSize = this->getInt(byteIndex);
                size_t byteSubIndex = byteIndex + Bytes::intSize;
                size_t yIndex = byteSubIndex + stringSize;
                std::vector<unsigned char> elements = this->slice(this->data,
                                                                  (int) byteSubIndex,
                                                                  (int) yIndex);
                char stringData[(4096 ^ 2)];
                memcpy(stringData, elements.data(), stringSize);
                stringData[stringSize] = '\0';
                std::string stringElement(stringData);
                this->index += stringSize;
                return stringElement;
            }

            /**
             * Returns the bytes at current index
             * @return Byte Data
             */
            std::vector<unsigned char> getBytes()
            {
                return this->getBytes(this->getIndex());
            };

            /**
             * Returns the bytes at given index
             * @param byteIndex Byte Index
             * @return Byte Data
             */
            std::vector<unsigned char> getBytes(size_t byteIndex)
            {
                int byteSize = this->getInt(byteIndex);
                size_t byteSubIndex = byteIndex + Bytes::intSize;
                size_t yIndex = byteSubIndex + byteSize;
                std::vector<unsigned char> elements = this->slice(this->data,
                                                                  (int) byteSubIndex,
                                                                  (int) yIndex);
                this->index += byteSize;
                return elements;
            }

            /**
             * Returns internal data as vector
             * @return VBytes vector
             */
            std::vector<unsigned char> toVector()
            {
                return {this->data};
            }

        private:
            size_t size = 0;
            size_t index = 0;
            std::vector<unsigned char> data{};

            /**
             * Slices a vector
             * @tparam T Vector Template
             * @param array Vector Array
             * @param X Slice Begin
             * @param Y Slice End
             * @return Sliced vector
             */
            std::vector<unsigned char > slice(std::vector<unsigned char> const& array, int X, int Y)
            {
                auto start = array.begin() + X;
                auto end = array.begin() + Y;
                std::vector<unsigned char> result(Y - X);
                std::copy(start, end, result.begin());
                return result;
            }
    };
}
#endif //SRC_BYTEBUFFER_H
