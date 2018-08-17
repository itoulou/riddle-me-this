import unittest
import run

class TestsLogin(unittest.TestCase):
    
    def test_save_user(self):
        """
        test to save username into a file
        """
        run.save_user("test")
       
       
        usernames = []
        with open("data/usernames.txt", "r") as usernames_file:
            usernames = usernames_file.readlines()
        print(usernames)
        self.assertNotEqual(len(usernames), 0)
        self.assertEqual(usernames[-1], "test\n")  
        
    
        
        
        
def main():
       unittest.main()
       
if __name__ == "__main__":
    main()