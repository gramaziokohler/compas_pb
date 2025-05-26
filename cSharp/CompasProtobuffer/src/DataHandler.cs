using System;
using System.Collections.Generic;
using System.IO;
using Google.Protobuf;
using Google.Protobuf.WellKnownTypes;
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

        public static void PBLoad(string filePath)
        {
            ValidateFilePath(filePath);
            Console.WriteLine($"Loading data from: {filePath}");

            byte[] byteData = File.ReadAllBytes(filePath);
            Console.WriteLine(byteData);
            var message = AnyData.Parser.ParseFrom(byteData);

            Console.WriteLine($"Root Any type: {message.Data.TypeUrl}");

            // The root should be DictData based on your data
            if (message.Data.Is(DictData.Descriptor))
            {
                var rootDict = message.Data.Unpack<DictData>();
                Console.WriteLine($"DictData: {rootDict}");
            }
            else
            {
                Console.WriteLine($"Expected DictData but got: {message.Data.TypeUrl}");
            }

            // Console.WriteLine($"Message descriptor: {message.Descriptor?.Name ?? "Unknown"}");

            // Any anyMessage = message.Data.Data;
            // Console.WriteLine(anyMessage.GetType());
            // var anyMessage = Any.Parser.ParseFrom(message.Data);
            // Any.Parser.
            // Console.WriteLine(anyMessage);
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
