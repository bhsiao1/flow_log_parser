import unittest
from unittest.mock import mock_open, patch
from parser import convert_lookup_table, map_flow_log, convert_output_to_file, main

class parser_test(unittest.TestCase):

    @patch("builtins.open", new_callable = mock_open, read_data = "dstport,protocol,tag\n25,tcp,sv_P1\n68,udp,sv_P2\n")
    def test_convert_lookup_table(self, mock_file):
        expected_lookup_table = {
            ('25','tcp'): 'sv_P1',
            ('68', 'udp'): 'sv_P2'
        }

        lookup_table = convert_lookup_table("lookup_table.csv")

        self.assertEqual(lookup_table, expected_lookup_table)

    @patch("builtins.open", new_callable=mock_open, read_data="2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK")
    def test_map_flow_log(self, mock_file):
        lookup_table = {('443', 'tcp'): 'sv_P2'}
        expected_output = {
            'sv_P2': 1,
            ('443', 'tcp'): 1
        }
        output = map_flow_log("flow_log.txt", lookup_table)
        self.assertEqual(output, expected_output)

    @patch("builtins.open", new_callable=mock_open)
    def test_convert_output_to_file(self, mock_file):
        result = {
            'sv_P2': 1,
            ('443', 'tcp'): 1
        }
        expected_output = "sv_P2,1\n"
        expected_output2 = "443,tcp,1\n"
        convert_output_to_file(result)
 
        mock_file().write.assert_any_call(expected_output)
        mock_file().write.assert_any_call(expected_output2)
    
    @patch("builtins.open", new_callable=mock_open, read_data="2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK")
    @patch("builtins.open", new_callable=mock_open, read_data="dstport,protocol,tag\n25,tcp,sv_P1\n68,udp,sv_P2\n")
    @patch("builtins.open", new_callable=mock_open)
    def test_main(self, mock_flow_log, mock_lookup_table, mock_output):
        main()

        mock_output().write.assert_called()

if __name__ == '__main__':
    unittest.main()