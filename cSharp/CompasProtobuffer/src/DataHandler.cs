using System;
using System.Collections.Generic;
using System.IO;
using Google.Protobuf;

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

        public static MessageData PBLoad(string filePath)
        {
            ValidateFilePath(filePath);
            Console.WriteLine($"Loading data from: {filePath}");

            byte[] byteData = File.ReadAllBytes(filePath);
            var data = ByteString.CopyFrom(byteData);
            MessageData message = MessageData.Parser.ParseFrom(byteData);
            Console.WriteLine($"{message.GetType().FullName}");
            return message;
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
