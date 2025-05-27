using System;
using CompasPb.Data;

namespace CompasPb.Data
{
    public class DataHandler
    {
        private static void ValidateFilePath(string filePath)
        {
            if (!File.Exists(filePath))
            {
                throw new FileNotFoundException($"File not found: {filePath}");
            }
        }

        public static AnyData PBLoad(string filePath)
        {
            ValidateFilePath(filePath);
            Console.WriteLine($"Loading data from: {filePath}");
            byte[] byteData = File.ReadAllBytes(filePath);
            MessageData message = MessageData.Parser.ParseFrom(byteData);
            return message.Data;
        }

        public static void PBdump() => Console.WriteLine("dump data to proto");

        public static void PBLoadJSON(string filePath)
        {
            ValidateFilePath(filePath);
            Console.WriteLine($"Loading JSON data from: {filePath}");
            // Implement JSON loading logic herek
        }

        public static void PBdumpJSON() => Console.WriteLine("dump data to JSON");

        public static void PBLoadBytes(string filePath)
        {
            ValidateFilePath(filePath);
            Console.WriteLine($"Loading data from: {filePath}");
            // Implement here
        }

        public static void PBdumpBytes() => Console.WriteLine("dump data to bytes");
    }
}
