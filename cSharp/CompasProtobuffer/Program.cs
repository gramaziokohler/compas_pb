using CompasPb.Data;
using Google.Protobuf;
using Google.Protobuf.WellKnownTypes;

class Program
{
    public static void Main(string[] args)
    {
        // DataHandler handler = new DataHandler();
        string currentPath = Directory.GetCurrentDirectory();
        string parentPath = Path.GetFullPath(Path.Combine(currentPath, @"..\.."));
        string filePath = Path.GetFullPath(Path.Combine(parentPath, @"examples\temp\nested_data.bin"));
        // filePath = @"C:\Users\ckasirer\repos\compas_pb\examples\temp\data_dict.bin";
        filePath = @"/Users/weitingchen/project/gkr/compas_pb/examples/temp/nested_data.bin";
        var data = DataHandler.PBLoad(filePath);
        Console.WriteLine(data.GetType());
        // if (data.Data.Is(DictData.Descriptor))
        // {
        //     var dictData = data.Data.Unpack<DictData>();
        //     Console.WriteLine($"DictData: {dictData}");
        // }
        // var datatype = DataProcesser.TryGetValue<Point>(data);
    }
}

// public class Program
//
//     public static void Main(string[] args)
//     {
//         Console.WriteLine("Compas Protocol Buffer");
//         string filePath;
//         if (args.Length > 0)
//         {
//             filePath = args[0];
//         }
//         else
//         {
//             filePath = @"C:\Users\ckasirer\repos\compas_pb\examples\temp\data_dict.bin";
//         }

//         AnyData data = CompasPbApi.pbLoad(filePath);
//         //AnyData? messageData = pbLoadBytes(filePath);
//         //AnyData? messageData = pbLoadJSON(filePath);

//         // var point = TryGetValue<Point>(data);
//         var listOfPoints = TryGetValue<List<Point>>(data);
//         // var dictOfStringsToPoints = TryGetValue<Dict<string, Point>>(data);
//         // var listOfWhatever = TryGetValue<List<AnyData>>(data); // we don't deal with deeper nesting levels, sue us.

//         foreach(var point in listOfPoints){
//             Console.WriteLine($"Item: {point.X: F2}, {point.Y:F2}, {point.Z:F2}");
//         }
//     }

// }

// class CompasPbApi
// {
//     public T TryGetValue<T>(AnyData obj)
//     {

//         throw new InvalidCastException($"Cannot cast {obj.GetType()} to {typeof(T)}");
//     }
//     // this is part of the COMPAS Protobuf csharp library
//     public static AnyData pbLoad(string filePath){
//         Console.WriteLine($"Processing file: {filePath}");
//         if (!File.Exists(filePath))
//         {
//             Console.WriteLine($"Error: File does not exist at path: {filePath}");
//             // raise exception!
//         }

//         // Abstract away file reading
//         byte[] data = File.ReadAllBytes(filePath);
//         var message = MessageData.Parser.ParseFrom(data);

//         // abstract away MessageData.Data
//         return message.Data;  // this can come from us
//     }

// }
