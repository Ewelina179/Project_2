import unittest
import server2


class TestSever2(unittest.TestCase):
    def test_uptime(self):
        begin=15
        end=20
        uptime=end-begin
        result=server2.uptime(end, begin)
        self.assertEqual(result, {'UPTIME': 5})

    def test_info(self):
        begin2=123
        server2.VERSION_OF_SERVER=112
        result=server2.info(begin2)
        self.assertEqual(result, {'INFO': {'DATE OF SERVER CREATION': 123, 'SERVER VERSION NUMBER': 112}})

    def test_help(self):
        result=server2.help()
        self.assertEqual(result, {"UPTIME":"cos", "INFO":"cos", "STOP":"cos", "LOG IN":"wez z wyzej"})

    

if __name__=="__main__":
    unittest.main()