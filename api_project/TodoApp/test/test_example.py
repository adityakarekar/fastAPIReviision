import pytest
def test_equal_or_not_equal():
    assert 3==3
    assert 3!=1

def test_is_instance():
    assert isinstance("this is a string",str)
    assert not isinstance("10",int)

def test_boolean():
    validate=True
    assert validate is True
    assert("hello"=="world") is False

def test_type():
    assert type("Hello" is str)
    assert type("World" is not int)

def test_list():
    num_list=[1,2,3,4,5]
    any_list=[False,False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)



class Student:
    def __init__(self,firstName:str,lastName:str,age:int):
        self.firstName=firstName
        self.lastName=lastName
        self.age=age

@pytest.fixture
def example_user():
    return Student("Aditya","Karekar",26)

def test_person_initialization(example_user):
    assert example_user.firstName=="Aditya"
    assert example_user.lastName=="Karekar"
    assert example_user.age==26