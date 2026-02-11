using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using WebApplication2.Repositories;

namespace WebApplication2.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PersonController : ControllerBase
    {
        static PersonRepository repo = new PersonRepository();
        // GET: api/Person
        [HttpGet]
        public IEnumerable<Person> Get()
        {
            return repo.GetPersons();
        }

        // GET: api/Person/5
        [HttpGet("{id}", Name = "Get")]
        public Person Get(int id)
        {
            return repo.GetPerson(id);
        }

        // POST: api/Person
        [HttpPost]
        public string Post(Person per)
        {
            repo.AddPerson(per);
            return "Created";
        }

        // PUT: api/Person/5
        [HttpPut("{id}")]
        public string Put(int id, Person per)
        {
            repo.UpdatePerson(per, id);
            return "Updated";
        }

        // DELETE: api/ApiWithActions/5
        [HttpDelete("{id}")]
        public string Delete(int id)
        {
            repo.DeletePerson( id);
            return "Deleted";
        }
    }
}
