using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebApplication2.Repositories
{
    public class PersonRepository
    {
        List<Person> persons = new List<Person>();

        public PersonRepository()
        {
            persons.Add(new Person(1, "Ron"));
            persons.Add(new Person(2, "Dana"));
        }

        public List<Person> GetPersons()
        {
            return persons;
        }

        public Person GetPerson(int id)
        {
            return persons.Where(x => x.ID == id).First();
        }

        public void AddPerson(Person per)
        {
             persons.Add(per);
        }

        public void UpdatePerson(Person per, int id)
        {
            Person pers = persons.Where(x => x.ID == id).First() ;
            pers.Name = per.Name;
        }

        public void DeletePerson( int id)
        {
            Person pers = persons.Where(x => x.ID == id).First();
            persons.Remove(pers);
        }
    }
}
