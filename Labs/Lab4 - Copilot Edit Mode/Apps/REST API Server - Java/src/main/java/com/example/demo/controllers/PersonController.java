package com.example.demo.controllers;

import com.example.demo.models.Person;
import com.example.demo.services.PersonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/persons")
public class PersonController {

    @Autowired
    private PersonService service;

    @GetMapping
    public List<Person> getAllPersons()
    {
        return service.getAllPersons();
    }

    @GetMapping("/{id}")
    public  Person getPerson(@PathVariable(value = "id") int personID)
    {
        return service.getPerson(personID);
    }

    @PostMapping
    public String createPerson(@RequestBody Person per)
    {
        service.addPerson(per);
        return "Created !";
    }

    @PutMapping("/{id}")
    public String updatePerson(@PathVariable(value="id") int perid, @RequestBody Person per)
    {
        service.updatePerson(perid, per);
        return "Updated !";
    }

    @DeleteMapping("/{id}")
    public String deletePerson(@PathVariable(value = "id") int perid)
    {
        service.deletePerson(perid);
        return "Deleted!";
    }
}
