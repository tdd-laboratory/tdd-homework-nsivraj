import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals1(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')
    def test_mixed_ordinals2(self):
        self.assert_extract('123,456,789', library.mixed_ordinals, '123', '456', '789')
    def test_mixed_ordinals3(self):
        self.assert_extract('5, 23, 93, 45', library.mixed_ordinals, '5', '23', '93', '45')


    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Fourth unit test; prove the code correctly extracts "2015-07-25" as a date from a sentence of text
    def test_date1(self):
        self.assert_extract("I was born on 2015-07-25.", library.dates_iso8601, '2015-07-25')
    def test_date2(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123.", library.dates_iso8601, '2018-06-22 18:22:19.123')
    def test_date3(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123.", library.dates_iso8601, '2018-06-22T18:22:19.123')
    def test_date4(self):
        self.assert_extract("I was born on 2018-06-22 18:22.", library.dates_iso8601, '2018-06-22 18:22')
    def test_date5(self):
        self.assert_extract("I was born on 2018-06-22 18:22:30 MDT.", library.dates_iso8601, '2018-06-22 18:22:30 MDT')
    def test_date6(self):
        self.assert_extract("I was born on 2018-06-22 18:22:31.231 Z.", library.dates_iso8601, '2018-06-22 18:22:31.231 Z')
    def test_date7(self):
        self.assert_extract("I was born on 2018-06-22 18:22:31.2314 -0800.", library.dates_iso8601)

    # Fifth unit test; prove that the code does not match sequences where the middle number
    # in the date is greater than 12 (December), or where the final number in the date is greater than 31.
    def test_no_month(self):
        self.assert_extract("I was born on 2015-13-25.", library.dates_iso8601)
    def test_no_day(self):
        self.assert_extract("I was born on 2015-11-32.", library.dates_iso8601)

    # Sixth unit test; prove the code correctly extracts "25 Jan 2017" as a date from a sentence of text
    def test_noniso_date1(self):
        self.assert_extract("I was born on 25 Jan 2017.", library.dates_noniso, '25 Jan 2017')
    # Seventh unit test; prove the code correctly extracts "25 Jun 2017" as a date from a sentence of text
    def test_noniso_date2(self):
        self.assert_extract("I was born on 25 Jun 2017.", library.dates_noniso, '25 Jun 2017')
    # Eighth unit test; prove the code correctly extracts "25 Mar 2017" as a date from a sentence of text
    def test_noniso_date3(self):
        self.assert_extract("I was born on 25 Mar 2017.", library.dates_noniso, '25 Mar 2017')
    # Ninth unit test; prove the code correctly extracts "25 May 2017" as a date from a sentence of text
    def test_noniso_date4(self):
        self.assert_extract("I was born on 25 May 2017.", library.dates_noniso, '25 May 2017')
    # Tenth unit test; prove the code does NOT extract "25 March 2017" as a date from a sentence of text
    def test_noniso_date5(self):
        self.assert_extract("I was born on 25 March 2017.", library.dates_noniso)
    # Eleventh unit test; prove the code correctly extracts "" as a date from a sentence of text
    def test_noniso_date6(self):
        self.assert_extract("I was born on 25 Jun, 2017.", library.dates_noniso, '25 Jun, 2017')


if __name__ == '__main__':
    unittest.main()
