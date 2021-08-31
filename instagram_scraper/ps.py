"""Parser and datastructure for PS Buildingblocks JSON files"""
# Needed in Python 3.9, should be removed in the future
from __future__ import annotations
import re
from abc import ABC, abstractmethod
from functools import reduce

class Expression(ABC):
    """Base class for all different expressions."""
    @staticmethod
    def from_json(json) -> Expression:
        """Create an expression from a JSON object.
        
        This method delegates to the specific expression subclass.
        """
        if json['type'] == 'TermExpression':
            return TermExpression.from_json(json)
        elif json['type'] == 'NotExpression':
            return NotExpression.from_json(json)
        elif json['type'] == 'AndExpression':
            return AndExpression.from_json(json)
        elif json['type'] == 'OrExpression':
            return OrExpression.from_json(json)
        elif json['type'] == 'LiteralExpression':
            return LiteralExpression.from_json(json)
        else:
            raise ValueError("Unknown expression %s" % json['type'])

    @abstractmethod
    def check(terms: list[str]) -> bool:
        """Returns true if the terms match the expression, needs to be implemented by the subclass"""
        raise NotImplementedError("This method needs to be implemented by the subclass.")


class TermExpression(Expression):
    """Most simple expression, matches on a single word."""
    def __init__(self, term: str) -> None:
        self.term = term
    
    @staticmethod
    def from_json(json) -> TermExpression:
        """Creates a term expression from a JSON object.""" 
        assert (json['type'] == 'TermExpression'), "Expression is of wrong type"
        return TermExpression(
            json['term']
        )
    
    def check(terms: list[str]) -> bool:
        """Returns true if any of the terms match this expression's term."""
        return self.term in terms


class NotExpression(Expression):
    """Inverts the result of the subexpression."""
    def __init__(self, expression: Expression) -> None:
        self.expression = expression
    
    @staticmethod
    def from_json(json) -> NotExpression:
        """Creates a not expression from a JSON object."""
        assert (json['type'] == 'NotExpression'), "Expression is of wrong type"
        return NotExpression(
            Expression.from_json(json['not'])
        )
    
    def check(terms: list[str]) -> bool:
        """Returns true if the subexpression is false."""
        return not self.expression.check(terms)


class AndExpression(Expression):
    """Combines the results of all subexpressions with the and operator."""
    def __init__(self, expressions: list[Expression]) -> None:
        self.expressions = expressions
    
    @staticmethod
    def from_json(json) -> AndExpression:
        """Creates a and expression from a JSON object."""
        assert (json['type'] == 'AndExpression'), "Expression is of wrong type"
        return AndExpression(
            [Expression.from_json(expression) for expression in json['and']]
        )
    
    def check(terms: list[str]) -> bool:
        """Returns true if all subexpressions are true."""
        for expr in self.expressions:
            if not expr.check(terms):
                return False
        return True


class OrExpression(Expression):
    """Combines the results of all subexpressions with the or operator."""
    def __init__(self, expressions: list[Expression]) -> None:
        self.expressions = expressions
    
    @staticmethod
    def from_json(json) -> OrExpression:
        """Creates an or expression from a JSON object."""
        assert (json['type'] == 'OrExpression'), "Expression is of wrong type"
        return OrExpression(
            [Expression.from_json(expression) for expression in json['or']]
        )
    
    def check(terms: list[str]) -> bool:
        """Returns true if any of the subexpressions are true."""
        for expr in self.expressions:
            if expr.check(terms):
                return True
        return False


class LiteralExpression(Expression):
    """Repeats the result of the subexpression.
    
    The use of this expression is unknown and it's implementation is a guess.
    """
    def __init__(self, expression: Expression) -> None:
        self.expression = expression
    
    @staticmethod
    def from_json(json) -> LiteralExpression:
        """Create a literal expression from a JSON object."""
        assert (json['type'] == 'LiteralExpression'), "Expression is of wrong type"
        return LiteralExpression(
            Expression.from_json(json['literal'])
        )
    
    def check(terms: list[str]) -> bool:
        """Returns the result of the subexpression."""
        # TODO: it's unknown what is actually supposed to happen here, so this is probably wrong
        return self.expression.check(terms)


class SearchTerm:
    """A collection of expressions that combine into a search term."""
    def __init__(self, expression: Expression, exclude: list[Expression]) -> None:
        self.expression = expression
        self.exclude = exclude

    @staticmethod
    def from_json(json) -> SearchTerm:
        """Create a search term from a JSON object."""
        return SearchTerm(
            Expression.from_json(json['expression']),
            [Expression.from_json(expression) for expression in json['exclude']]
        )
    
    def check(self, terms: list[str]) -> bool:
        """Returns true if the terms don't match the exclusions but do match the expression."""
        for expr in self.exclude_search_terms:
            if expr.check(terms):
                return False
        return self.expression.check(terms)


class PSBuildingblock:
    """A collection of search terms for a specific purpose."""
    def __init__(self, name: str, language: str, search_terms: list[SearchTerm], exclude_search_terms: list[SearchTerm]) -> None:
        self.name = name
        self.language = language
        self.search_terms = search_terms
        self.exclude_search_terms = exclude_search_terms
    
    @staticmethod
    def from_json(json) -> PSBuildingblock:
        """Create a building block from a JSON object."""
        return PSBuildingblock(
            json['name'],
            json['language'],
            [SearchTerm.from_json(term) for term in json['searchTerms']],
            [SearchTerm.from_json(term) for term in json['excludeSearchTerms']]
        )

    def check(self, terms: list[str]) -> bool:
        """Returns true if the terms don't match the exclusions but do match a search term."""
        for search in exclude_search_terms:
            if search.check(terms):
                return False
        for search in search_terms:
            if search.check(terms):
                return True


class PS:
    """A collection of buildingblocks for various search purposes."""
    def __init__(self, buildingblocks: list[PSBuildingblock]):
        self.buildingblocks = buildingblocks
    
    @staticmethod
    def from_json(json) -> PS:
        """Create the PS from a JSON document."""
        return PS(
            [PSBuildingblock.from_json(bb) for bb in json]
        )
    
    def merge(other: PS):
        """Merge two PS into one."""
        self.buildingblocks.extend(PS.buildingblocks)
    
    def match(terms: list[str]) -> list[PSBuildingblock]:
        """Returns which buildingblocks match on these terms."""
        results = []
        for bb in self.buildingblocks:
            if bb.check(terms):
                results.append(bb)
        return results
