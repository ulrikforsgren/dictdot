#!/usr/bin/env python3

import unittest
from dictdot.dict_dot import Map


class TestMap(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_data = {
            'desc': "This is just a test",
            'kalle': {
                'touched': True,
                'value': 1
            },
            'olle': {
                'touched': False,
                'value': 4
            }
        }
        self.map = Map(self.sample_data.copy())

    def test_initialization(self):
        """Test Map initialization with different parameters."""
        # Test initialization with dict
        m = Map({'a': 1, 'b': 2})
        self.assertEqual(m.data, {'a': 1, 'b': 2})
        
        # Test initialization with None
        m = Map()
        self.assertEqual(m.data, {})
        
        # Test initialization with invalid type
        with self.assertRaises(TypeError):
            Map([1, 2, 3])

    def test_attribute_access(self):
        """Test attribute access on Map objects."""
        # Test existing attributes
        self.assertEqual(self.map.desc, "This is just a test")
        self.assertEqual(self.map.kalle.touched, True)
        self.assertEqual(self.map.kalle.value, 1)
        self.assertEqual(self.map.olle.touched, False)
        self.assertEqual(self.map.olle.value, 4)
        
        # Test non-existing attributes
        self.assertEqual(str(self.map.non_existent), "")
        self.assertEqual(repr(self.map.non_existent), "Map <non-existing>")
        self.assertEqual(str(self.map.non_existent.nested), "")
        
        # Test bool conversion
        self.assertTrue(self.map.kalle)  # Non-empty dict is truthy
        self.assertFalse(self.map.non_existent)  # Non-existing is falsy
        
        # Test int conversion
        self.assertEqual(int(self.map.kalle), 2)  # 2 items in kalle dict
        self.assertEqual(int(self.map.non_existent), 0)  # Non-existing has length 0

    def test_attribute_assignment(self):
        """Test attribute assignment on Map objects."""
        # Test simple assignment
        self.map.new_attr = "test"
        self.assertEqual(self.map.new_attr, "test")
        
        # Test nested assignment
        self.map.nested.attr = 42
        self.assertEqual(self.map.nested.attr, 42)
        
        # Test dictionary assignment
        self.map.dict_attr = {'a': 1, 'b': 2}
        self.assertEqual(self.map.dict_attr.a, 1)
        self.assertEqual(self.map.dict_attr.b, 2)

    def test_item_access(self):
        """Test dictionary-style item access."""
        # Test existing items
        self.assertEqual(self.map['desc'], "This is just a test")
        self.assertEqual(self.map['kalle']['touched'], True)
        
        # Test item assignment
        self.map['new_item'] = 'value'
        self.assertEqual(self.map['new_item'], 'value')
        
        # Test nested item assignment requires the nested dict to exist first
        self.map['nested'] = {}
        self.map['nested']['item'] = 'nested_value'
        self.assertEqual(self.map['nested']['item'], 'nested_value')

    def test_contains(self):
        """Test 'in' operator."""
        self.assertIn('desc', self.map)
        self.assertIn('kalle', self.map)
        self.assertNotIn('non_existent', self.map)
        
        # Test nested 'in'
        self.assertIn('touched', self.map.kalle)
        self.assertIn('value', self.map.kalle)

    def test_merge(self):
        """Test merging of Map objects."""
        # Test simple merge with Map objects
        a = Map({'a': 1, 'b': 2})
        b = Map({'c': 3, 'd': 4})
        a.merge(b)
        self.assertEqual(a.data, {'a': 1, 'b': 2, 'c': 3, 'd': 4})
        
        # Test merge with dict (should work since merge handles dict conversion)
        a = Map({'a': 1})
        b = {'b': 2}
        a.merge(b)
        self.assertEqual(a.data, {'a': 1, 'b': 2})
        
        # Test merge with nested dicts
        a = Map({'x': {'a': 1, 'b': 2}})
        b = Map({'x': {'b': 3, 'c': 4}})
        a.merge(b)
        self.assertEqual(a.data, {'x': {'a': 1, 'b': 3, 'c': 4}})
        
        # Test merge with incompatible types
        a = Map({'a': 1})
        b = Map({'a': 'string'})
        with self.assertRaises(TypeError):
            a.merge(b)


    def test_items_and_keys(self):
        """Test items() and keys() methods."""
        # Test items()
        items = list(self.map.items())
        self.assertIn(('desc', "This is just a test"), items)
        self.assertIn(('kalle', self.map.kalle.data), items)
        
        # Test keys()
        keys = list(self.map.keys())
        self.assertIn('desc', keys)
        self.assertIn('kalle', keys)
        self.assertIn('olle', keys)

    def test_as_dict(self):
        """Test conversion to dictionary."""
        # Create a complex Map structure
        m = Map()
        m.a = 1
        m.b = {'x': 2, 'y': Map({'z': 3})}
        m.c = [1, 2, {'a': 1, 'b': Map({'c': 2})}]
        
        # Convert to dict
        d = m.as_dict()
        
        # Verify the structure and types
        self.assertEqual(d['a'], 1)
        self.assertIsInstance(d['b'], dict)
        self.assertEqual(d['b']['x'], 2)
        self.assertIsInstance(d['b']['y'], dict)  # Should be dict, not Map
        self.assertEqual(d['b']['y']['z'], 3)
        self.assertEqual(d['c'][0], 1)
        self.assertEqual(d['c'][1], 2)
        self.assertIsInstance(d['c'][2], dict)
        self.assertEqual(d['c'][2]['a'], 1)
        self.assertIsInstance(d['c'][2]['b'], dict)  # Should be dict, not Map
        self.assertEqual(d['c'][2]['b']['c'], 2)

    def test_edge_cases(self):
        """Test edge cases and special scenarios."""
        # Test empty Map
        m = Map()
        self.assertEqual(str(m), "{}")
        self.assertEqual(repr(m), "Map {}")
        self.assertFalse(m)
        
        # Test None values
        m.none_val = None
        # In the current implementation, None values are treated as non-existent
        # and accessing them returns a Map with a backpointer
        self.assertIn('none_val', m)  # The key exists in the data dict
        self.assertEqual(str(m.none_val), '')  # str(non-existent) returns empty string
        self.assertEqual(repr(m.none_val), 'Map <non-existing>')  # repr shows non-existing state
        
        # Test list access and modification
        m.list_val = [1, 2, 3]
        self.assertEqual(m.list_val[0], 1)
        m.list_val.append(4)
        self.assertEqual(m.list_val, [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()
