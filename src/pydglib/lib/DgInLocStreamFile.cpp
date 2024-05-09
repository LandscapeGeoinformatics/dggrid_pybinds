/*******************************************************************************
    Copyright (C) 2023 Kevin Sahr

    This file is part of DGGRID.

    DGGRID is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    DGGRID is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*******************************************************************************/
////////////////////////////////////////////////////////////////////////////////
//
// DgInLocStreamFile.cpp: DgInLocStreamFile class implementation
//
////////////////////////////////////////////////////////////////////////////////

#include "dglib/DgInLocStreamFile.h"
#include <iterator>

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
DgInLocStreamFile::DgInLocStreamFile(const DgRFBase& rfIn,
                                     std::vector<std::string> &array,
                                     const string* fileNameIn,
                                     bool isPointFileIn,
                                     DgReportLevel failLevel)
         : DgInLocFile (rfIn, fileNameIn, isPointFileIn, failLevel),
           degRF_ (nullptr)
{
    this->DATA.resize(array.size());
    this->DATA.assign(array.begin(), array.end());
   if (fileNameIn)
      if (!open(NULL, DgBase::Silent) && this->DATA.empty())
      {
         report("DgInLocStreamFile::DgInLocStreamFile() unable to open file " +
                fileName_, failLevel);
      }

} // DgInLocStreamFile::DgInLocStreamFile

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
bool
DgInLocStreamFile::open (const string *fileNameIn, DgReportLevel failLevel)
//
// Open fileName as an input file. Report with a report level of failLevel
// if the open is unsuccessful.
//
// Returns true if successful and false if unsuccessful.
//
{
    if (fileNameIn)
        fileName_ = *fileNameIn;
   // make sure we are not already open
   if (this->DATA.empty())
   {
       std::string line;
       std::ifstream file(fileName_.c_str(), ios::in);
       if (!file.good())
       {
           report("DgInLocStreamFile::open() unable to open file " + fileName_, failLevel);
           return false;
       }
       while (std::getline(file, line)) { *this << line << std::endl; }
   }
   else { for (auto n : this->DATA) { *this << n << std::endl; } }
    return true;
} // DgInLocStreamFile::open

////////////////////////////////////////////////////////////////////////////////
