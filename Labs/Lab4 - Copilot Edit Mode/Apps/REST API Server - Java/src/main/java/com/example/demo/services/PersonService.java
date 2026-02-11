package com.example.demo.services;

import com.example.demo.models.Person;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class PersonService {

    private List<Person> persons;

    public PersonService()
    {
        this.persons = new ArrayList<>();

        Person per1 = new Person();
        per1.id = 1;
        per1.name = "Ron";
        per1.age = 20;
        per1.city = "Jerusalem";

        Person per2 = new Person();
        per2.id = 2;
        per2.name = "Dana";
        per2.age = 25;
        per2.city = "Eilat";

        persons.add(per1);
        persons.add(per2);


    }

    public List<Person> getAllPersons()
    {
        return this.persons;
    }

    public Person getPerson(int id)
    {
        return this.persons.stream().filter(x -> x.id == id).collect(Collectors.toList()).get(0);
    }

    public void addPerson(Person per)
    {
        persons.add(per);
    }

    public void updatePerson(int id, Person per)
    {
        Person p =  this.persons.stream().filter(x -> x.id == id).collect(Collectors.toList()).get(0);
        p.name = per.name;
        p.city = per.city;
        p.age = per.age;
    }

    public void deletePerson(int id)
    {
        Person p =  this.persons.stream().filter(x -> x.id == id).collect(Collectors.toList()).get(0);
        persons.remove(p);

    }
}
