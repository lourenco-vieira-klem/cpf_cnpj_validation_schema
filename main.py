from marshmallow import Schema, ValidationError, validates_schema, fields, validate
import sys


class BaseValidator():
    def get_digits(self, document: str) -> list:
        return [int(digit) for digit in document if digit.isdigit()]
    
    def raise_error(self, document_type: str) -> None:
        raise ValidationError(
            field_name=document_type,
            message="Invalid document."
        )
    
    def check_if_all_digits_are_equals(self, document: list, document_type: str) -> None:
        if all(digit == document for digit in document):
            self.raise_error(document_type)

class CPFValidator(BaseValidator):
    @validates_schema
    def validate_cpf(self, data, **kwargs):
        cpf = self.get_digits(data['cpf'])
        self.check_if_all_digits_are_equals(cpf, 'CPF')
        
        for i in range(9, 11):
            value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                self.raise_error(document_type='CPF')

class CNPJValidator(BaseValidator):
    @validates_schema
    def validate_cnpj(self, data, **kwargs):
        first_multiplication = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        second_multiplication = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        cnpj = self.get_digits(data['cnpj'])
        self.check_if_all_digits_are_equals(cnpj, 'CNPJ')
        
        value = sum((cnpj[i] * first_multiplication[i] for i in range(0, 12))) % 11
        first_digit = 0 if value < 2 else 11 - value
        value = sum((cnpj[i] * second_multiplication[i] for i in range(0, 13))) % 11
        second_digit = 0 if value < 2 else 11 - value
        
        if (cnpj[12] != first_digit or cnpj[13] != second_digit):
            self.raise_error('CNPJ')

class CPFSchema(Schema, CPFValidator):
    cpf = fields.String(required=True, validate=[validate.Length(equal=11)])

class CNPJSchema(Schema, CNPJValidator):
    cnpj = fields.String(required=True, validate=[validate.Length(equal=14)])

def validate_cpf(cpf):
    try:
        cpf_schema = CPFSchema()
        result = cpf_schema.validate({'cpf': cpf})
        
        if result:
            print("Invalid CPF.")
        else:
            print("CPF is valid.")
        
    except Exception as ex:
        print(ex)

def validate_cnpj(cnpj):
    try:
        cnpj_schema = CNPJSchema()
        result = cnpj_schema.validate({'cnpj': cnpj})
        
        if result:
            print("Invalid CNPJ.")
        else:
            print("CNPJ is valid.")
        
    except Exception as ex:
        print(ex)

if  __name__ == "__main__":
    argv = sys.argv[1]

    if len(argv) == 11:
        validate_cpf(argv)
    
    elif len(argv) == 14:
        validate_cnpj(argv)
    
    else:
        print("insert a valid CPF or CNPJ")
