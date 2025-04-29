using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using CompasPb.Data;
using CompasPb.Data.Processor;
using Google.Protobuf;


public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Compas Protocol Buffer");
        string filePath;
        if (args.Length > 0)
        {
            filePath = args[0];
        }
        else
        {
            filePath = Path.Combine(Directory.GetCurrentDirectory(), "..", "..", "examples", "temp", "nested_data.bin");
            filePath = Path.GetFullPath(filePath);
        }
        Console.WriteLine($"Processing file: {filePath}");
        if (!File.Exists(filePath))
        {
            Console.WriteLine($"Error: File does not exist at path: {filePath}");
            return;
        }

        byte[] data = File.ReadAllBytes(filePath);
        DataDeserializer dataDeserializer = new DataDeserializer(data);
        dynamic deserializedData = dataDeserializer.DeserializeMessage();

        Console.WriteLine($"Data Type: {deserializedData.GetType()}");
        // Console.WriteLine("\nPress any key to exit...");
        // Console.ReadKey();
    }
}

// public class ProtoBufProcessor
// {
//     public void ProcessProtoMessage(string filePath)
//     {
//         try
//         {
//             byte[] data = File.ReadAllBytes(filePath);
//             var message = CompasPb.Data.MessageData.Parser.ParseFrom(data);
//
//             Console.WriteLine($"Message Type: {message.GetType()}\n");
//             Console.WriteLine($"Message: {message}\n");
//
//             // convert to JSON using Google's built-in formatter
//             string jsonString = Google.Protobuf.JsonFormatter.Default.Format(message);
//             Console.WriteLine($"JSON representation:\n{jsonString}\n");
//
//             var options = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase, WriteIndented = true };
//             // Deserialize JSON to a dictionary
//             var dictionary = JsonSerializer.Deserialize<Dictionary<string, object>>(jsonString, options);
//             if (dictionary == null)
//             {
//                 Console.WriteLine("Failed to deserialize JSON to dictionary.");
//                 return;
//             }
//             Console.WriteLine("Full message as dictionary:");
//             Console.WriteLine(dictionary.GetType());
//             foreach (var entry in dictionary)
//             {
//                 Console.WriteLine($"{entry.Key}: {entry.Value}");
//             }
//             // print nested data
//             if (dictionary.TryGetValue("data", out object dataObj))
//             {
//                 var dataJson = JsonSerializer.Serialize(dataObj, options);
//                 Console.WriteLine($"\nNested Data Type: {dataJson.GetType()}");
//                 Console.WriteLine($"Nested Data: {dataJson}");
//             }
//         }
//         catch (Exception ex)
//         {
//             Console.WriteLine($"Error processing file: {ex.Message}");
//             Console.WriteLine($"Stack trace: {ex.StackTrace}");
//         }
//     }
//
// }
