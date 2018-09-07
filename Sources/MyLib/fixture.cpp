#include <MyLib/fixture.h>

#include <iostream>

namespace mylib
{
    void MyFixture::setUp()
    {
	   std::cout << "MyFixture::setUp()\n";
    }
}
