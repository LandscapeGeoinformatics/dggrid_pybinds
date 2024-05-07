#ifndef SRC_DGOWSTREAM_H
#define SRC_DGOWSTREAM_H
#include <ostream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <map>

class DgOWStream : public std::ostream
{
    public:
        std::string ID;
        std::vector<unsigned char> BYTES;

        DgOWStream(const std::string &fileId) : std::ostream(nullptr)
        {
            this->open(fileId);
        };

        ~DgOWStream() override{};

        DgOWStream *open(const std::string fileId)
        {
            this->ID = fileId;
            this->BYTES.clear();
            return this;
        }

        DgOWStream *clear()
        {
            this->BYTES.clear();
            return this;
        }

//        template <typename T>
//        friend DgOWStream& operator<<(DgOWStream& out, const T& value);
//
//        // Additional overload to handle ostream specific io manipulators
//        friend DgOWStream& operator<<(DgOWStream& out, std::ostream& (*func)(std::ostream&))
//        {
//            static_cast<std::ostream&>(out) << func;
//            return out;
//        }

        // Additional overload to handle ostream specific io manipulators
//        friend DgOWStream& operator<<(DgOWStream& out, std::string& string)
//        {
//            std::cout << string;
//            return out;
//        }

        // Accessor function to get a reference to the ostream
        std::ostream& get_ostream() { return *this; }
};

inline DgOWStream& operator<< (DgOWStream& file, const char* str)
{
    std::string stringData = std::string(str);
    file.BYTES.insert(
            file.BYTES.end(),
            stringData.begin(),
            stringData.end());
    return file;
}

inline DgOWStream& operator<< (DgOWStream& file, const std::string& stringData)
{
    file.BYTES.insert(
            file.BYTES.end(),
            stringData.begin(),
            stringData.end());
    return file;
}

inline DgOWStream& operator<< (DgOWStream& file, long double val)
{
    std::string data = std::to_string(val);
    file << data;
    return file;
}

inline DgOWStream& operator<< (DgOWStream& file, float val)
{
    std::string data = std::to_string(val);
    file << data;
    return file;
}

inline DgOWStream& operator<< (DgOWStream& file, int val)
{
    std::string data = std::to_string(val);
    file << data;
    return file;
}
#endif //SRC_DGOWSTREAM_H
