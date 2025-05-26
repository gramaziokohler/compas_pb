using System;
using System.IO;
using CompasPb.Data;

namespace CompasPb.Data
{
    public class DataHandler
    {
        private static void ValidateFilePath(string filePath)
        {
            if (filePath == null)
            {
                throw new ArgumentNullException(nameof(filePath), "Please provide file path.");
            }
        }
        public static MessageData PBLoad(string filePath)
        {

            ValidateFilePath(filePath);
            Console.WriteLine($"Loading data from: {filePath}");
            // Implement JSON loading logic here
            MessageData data = new MessageData();
            return data;
        }
        public static void PBdump() => Console.WriteLine("dump data to proto");

        public static void PBLoadJSON(string filePath)
        {
            ValidateFilePath(filePath);
            Console.WriteLine($"Loading JSON data from: {filePath}");
            // Implement JSON loading logic here
        }
        public static void PBdumpJSON() => Console.WriteLine("dump data to JSON");

        public static void PBLoadBytes(string filePath)
        {
            ValidateFilePath(filePath);
            Console.WriteLine($"Loading data from bytes: {filePath}");
            // Implement byte loading logic here
        }
        public static void PBdumpBytes() => Console.WriteLine("dump data to bytes");
    }
}
