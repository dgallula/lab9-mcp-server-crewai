using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebApplication2
{
    public class Person
    {
        public int ID { get; set; }
        public string Name { get; set; }

        public Person(int iD, string name)
        {
            ID = iD;
            Name = name;
        }
    }
}
