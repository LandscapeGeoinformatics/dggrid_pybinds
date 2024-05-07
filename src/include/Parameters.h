#ifndef SRC_PYDGGRID_PARAMETERS_H
#define SRC_PYDGGRID_PARAMETERS_H
#include "Functions.h"
#include "Constants.h"
#include <map>
#include <utility>

namespace pydggrid
{
    class Parameters
    {
        public:

            /**
             * Defines an options parameter
             * @param name Parameter Name
             * @param defaultValue Default Value
             * @param optionArray Options Array
             * @return Parameters Object
             */
            Parameters *define(const char *name,
                               const char *defaultValue,
                               std::vector<std::string> optionArray)
            {
                this->indexes.emplace_back(std::string(name));
                this->types[name] = Constants::DataTypes::OPTIONS;
                this->data[name] = std::any(defaultValue);
                this->options[name] = std::vector<std::string>(std::move(optionArray));
                this->limit[name] = std::pair<std::any, std::any>(0, 0);
                return this;
            };

            /**
             * Defines a string parameter
             * @param name Parameter Name
             * @param defaultValue Default Value
             * @return Parameters Object
             */
            Parameters *define(const char *name,
                               const char *defaultValue)
            {
                this->indexes.emplace_back(std::string(name));
                this->types[name] = Constants::DataTypes::OPTIONS;
                this->data[name] = std::any(defaultValue);
                this->options[name] = std::vector<std::string>{};
                this->limit[name] = std::pair<std::any, std::any>(0, 0);
                return this;
            };

            /**
             * Defines a 32 bit integer parameter
             * @param name Parameter Name
             * @param defaultValue Default Value
             * @param minValue Minimum Value
             * @param maxValue Maximum Value
             * @return Parameters Object
             */
            Parameters *define(const char *name,
                               int32_t defaultValue,
                               int32_t minValue,
                               int32_t maxValue)
            {
                this->indexes.emplace_back(std::string(name));
                this->types[name] = Constants::DataTypes::OPTIONS;
                this->data[name] = std::any(defaultValue);
                this->options[name] = std::vector<std::string>{};
                this->limit[name] = std::pair<std::any, std::any>(minValue, maxValue);
                return this;
            };

            /**
             * Defines a 64 bit integer parameter
             * @param name Parameter Name
             * @param defaultValue Default Value
             * @param minValue Minimum Value
             * @param maxValue Maximum Value
             * @return Parameters Object
             */
            Parameters *define(const char *name,
                               uint64_t defaultValue,
                               uint64_t minValue,
                               uint64_t maxValue)
            {
                this->indexes.emplace_back(std::string(name));
                this->types[name] = Constants::DataTypes::INT64;
                this->data[name] = std::any(defaultValue);
                this->options[name] = std::vector<std::string>{};
                this->limit[name] = std::pair<std::any, std::any>(minValue, maxValue);
                return this;
            };

            /**
             * Defines a double parameter
             * @param name Parameter Name
             * @param defaultValue Default Value
             * @param minValue Minimum Value
             * @param maxValue Maximum Value
             * @return Parameters Object
             */
            Parameters *define(const char *name,
                               double defaultValue,
                               double minValue,
                               double maxValue)
            {
                this->indexes.emplace_back(std::string(name));
                this->types[name] = Constants::DataTypes::DOUBLE;
                this->data[name] = std::any(defaultValue);
                this->options[name] = std::vector<std::string>{};
                this->limit[name] = std::pair<std::any, std::any>(minValue, maxValue);
                return this;
            };

            /**
             * Defines a boolean parameter
             * @param name Parameter Name
             * @param defaultValue Default Value
             * @return Parameters Object
             */
            Parameters *define(const char *name, bool defaultValue)
            {
                this->indexes.emplace_back(std::string(name));
                this->types[name] = Constants::DataTypes::BOOLEAN;
                this->data[name] = std::any(defaultValue);
                this->options[name] = std::vector<std::string>{};
                this->limit[name] = std::pair<std::any, std::any>(0, 0);
                return this;
            };

            /**
             * Saves a string value to the parameters
             * @param parameterName Parameter Name
             * @param parameterValue Parameter Value
             * @return Parameters Object
             */
            Parameters *save(const char *parameterName, const char *parameterValue)
            {
                if (!this->isParameter(parameterName))
                {
                    Functions::throw_error("Invalid parameter request -> {}", parameterName);
                    // OPTIONS TYPE
                    if (this->getType(parameterName) == Constants::DataTypes::OPTIONS)
                    {
                        if (!Functions::contains(this->options[parameterName],
                                                 std::string(parameterValue)))
                        {
                            Functions::throw_error(
                                    "Option {} doesn't exist for parameter {}",
                                    parameterValue,
                                    parameterName);
                        }
                        this->data[parameterName] = std::any(std::string(parameterValue));
                        return this;
                    }
                    // STRING TYPE
                    if (this->getType(parameterName) == Constants::DataTypes::STRING)
                    {
                        this->data[parameterName] = std::any(std::string(parameterValue));
                        return this;
                    }
                    // 32BIT INTEGER TYPE
                    if (this->getType(parameterName) == Constants::DataTypes::INT32)
                    {
                        int32_t value_t = std::stoi(std::string(parameterValue));
                        if (value_t < std::any_cast<int32_t>(this->limit[parameterName].first) ||
                            value_t > std::any_cast<int32_t>(this->limit[parameterName].second))
                        {
                            Functions::throw_error(
                                    "Invalid value ({}) for parameter {}, value must be between {} and {}",
                                    value_t,
                                    parameterName,
                                    std::any_cast<int32_t>(this->limit[parameterName].first),
                                    std::any_cast<int32_t>(this->limit[parameterName].second));
                        }
                        this->data[parameterName] = std::any(value_t);
                        return this;
                    }
                    // 64BIT INTEGER TYPE
                    if (this->getType(parameterName) == Constants::DataTypes::INT64)
                    {
                        uint64_t value_t = std::stoul(std::string(parameterValue));
                        if (value_t < std::any_cast<uint64_t>(this->limit[parameterName].first) ||
                            value_t > std::any_cast<uint64_t>(this->limit[parameterName].second))
                        {
                            Functions::throw_error(
                                    "Invalid value ({}) for parameter {}, value must be between {} and {}",
                                    value_t,
                                    parameterName,
                                    std::any_cast<uint64_t>(this->limit[parameterName].first),
                                    std::any_cast<uint64_t>(this->limit[parameterName].second));
                        }
                        this->data[parameterName] = std::any(value_t);
                        return this;
                    }
                    // DOUBLE TYPE
                    if (this->getType(parameterName) == Constants::DataTypes::DOUBLE)
                    {
                        double value_t = std::stod(std::string(parameterValue));
                        if (value_t < std::any_cast<double>(this->limit[parameterName].first) ||
                            value_t > std::any_cast<double>(this->limit[parameterName].second))
                        {
                            Functions::throw_error(
                                    "Invalid value ({}) for parameter {}, value must be between {} and {}",
                                    value_t,
                                    parameterName,
                                    std::any_cast<double>(this->limit[parameterName].first),
                                    std::any_cast<double>(this->limit[parameterName].second));
                        }
                        this->data[parameterName] = std::any(value_t);
                        return this;
                    }
                    // BOOLEAN TYPE
                    if (this->getType(parameterName) == Constants::DataTypes::BOOLEAN)
                    {
                        bool value_t = (std::string(parameterValue) == "true" ||
                                std::string(parameterValue) == "1");
                        this->data[parameterName] = std::any(value_t);
                        return this;
                    }
                    Functions::throw_error("Unimplemented Data type for parameter: {}", parameterName);
                }
                return this;
            };

            /**
             * Reads string parameters from a map dictionary
             * @param parameters Parameters Dictionary of parameters as {name, value}
             * @param
             */
            Parameters *read(const std::map<std::string, std::string>& parameterMap)
            {
                for (const auto& parameter : parameterMap)
                {
                    this->save(parameter.first.c_str(),
                               parameter.second.c_str());
                }
                return this;
            };

            /**
             * Returns true if parameter exists
             * @param parameterName Parameter Name
             * @return True if parameter exists
             */
            bool isParameter(const char *parameterName)
            {
                return Functions::contains(this->indexes, std::string (parameterName));
            };

            /**
             * Returns parameter type by name
             * @param parameterName Parameter Name
             * @return Parameter Type as Constants::DataType
             */
            int getType(const char *parameterName)
            {
                return (this->isParameter(parameterName)) ?
                    this->types[parameterName] : Constants::DataTypes::NONE;
            };

            /**
             * Returns string value of a parameter
             * @param parameterName Parameter Name
             * @return String value
             */
            std::string getString(const char *parameterName)
            {
                if (!this->isParameter(parameterName))
                {
                    Functions::throw_error("invalid parameter requested as string {}",
                                           parameterName);
                }
                if ((this->getType(parameterName) != Constants::DataTypes::STRING) &&
                    (this->getType(parameterName) != Constants::DataTypes::OPTIONS))
                {
                    Functions::throw_error("The requested parameter cannot be converted to string {}",
                                           parameterName);
                }
                return std::any_cast<std::string>(this->data[parameterName]);
            }

            /**
             * Returns 32bit integer value of a parameter
             * @param parameterName Parameter Name
             * @return 32bit Integer value
             */
            int32_t getInt32(const char *parameterName)
            {
                if (!this->isParameter(parameterName))
                {
                    Functions::throw_error("invalid parameter requested as 32 bit integer {}",
                                           parameterName);
                }
                if ((this->getType(parameterName) != Constants::DataTypes::INT32))
                {
                    Functions::throw_error("The requested parameter cannot be converted to 32 bit integer {}",
                                           parameterName);
                }
                return std::any_cast<int32_t>(this->data[parameterName]);
            }

            /**
             * Returns 64bit integer value of a parameter
             * @param parameterName Parameter Name
             * @return 64bit Integer value
             */
            int64_t getInt64(const char *parameterName)
            {
                if (!this->isParameter(parameterName))
                {
                    Functions::throw_error("invalid parameter requested as 64bit integer {}",
                                           parameterName);
                }
                if ((this->getType(parameterName) != Constants::DataTypes::INT64))
                {
                    Functions::throw_error("The requested parameter cannot be converted to 64bit integer {}",
                                           parameterName);
                }
                return std::any_cast<int64_t>(this->data[parameterName]);
            }

            /**
             * Returns double value of a parameter
             * @param parameterName Parameter Name
             * @return Double value
             */
            double getDouble(const char *parameterName)
            {
                if (!this->isParameter(parameterName))
                {
                    Functions::throw_error("invalid parameter requested as double {}",
                                           parameterName);
                }
                if ((this->getType(parameterName) != Constants::DataTypes::DOUBLE))
                {
                    Functions::throw_error("The requested parameter cannot be converted to double {}",
                                           parameterName);
                }
                return std::any_cast<double>(this->data[parameterName]);
            }

            /**
             * Returns boolean value of a parameter
             * @param parameterName Parameter Name
             * @return Boolean value
             */
            bool getBool(const char *parameterName)
            {
                if (!this->isParameter(parameterName))
                {
                    Functions::throw_error("invalid parameter requested as boolean {}",
                                           parameterName);
                }
                if ((this->getType(parameterName) != Constants::DataTypes::BOOLEAN))
                {
                    Functions::throw_error("The requested parameter cannot be converted to boolean {}",
                                           parameterName);
                }
                return std::any_cast<bool>(this->data[parameterName]);
            }



        private:
            std::map<std::string, int> types;
            std::vector<std::string> indexes;
            std::map<std::string, std::any> data;
            std::map<std::string, std::vector<std::string> > options;
            std::map<std::string, std::pair<std::any, std::any> > limit;

    };
}
#endif //SRC_PYDGGRID_PARAMETERS_H
