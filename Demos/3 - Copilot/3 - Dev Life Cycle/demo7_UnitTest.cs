using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.IO;

namespace DemoTests
{
    [TestClass]
    public class AddMethodTests
    {
        [TestMethod]
        public void Test_Add_PositiveNumbers()
        {
            using (var sw = new StringWriter())
            {
                Console.SetOut(sw);
                Add(3, 5);
                Assert.AreEqual("8\r\n", sw.ToString());
            }
        }

        [TestMethod]
        public void Test_Add_NegativeNumbers()
        {
            using (var sw = new StringWriter())
            {
                Console.SetOut(sw);
                Add(-3, -5);
                Assert.AreEqual("-8\r\n", sw.ToString());
            }
        }

        [TestMethod]
        public void Test_Add_PositiveAndNegativeNumbers()
        {
            using (var sw = new StringWriter())
            {
                Console.SetOut(sw);
                Add(10, -4);
                Assert.AreEqual("6\r\n", sw.ToString());
            }
        }

        [TestMethod]
        public void Test_Add_Zero()
        {
            using (var sw = new StringWriter())
            {
                Console.SetOut(sw);
                Add(0, 0);
                Assert.AreEqual("0\r\n", sw.ToString());
            }
        }

        // Helper method to call the static Add method
        private void Add(int a, int b)
        {
            demo7_UnitTest.Add(a, b);
        }
    }
}
