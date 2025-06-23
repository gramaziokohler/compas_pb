using CompasPb.Data;
using CompassPb.Data;
using Google.Protobuf;
using Google.Protobuf.WellKnownTypes;

class Program
{
    public static void Main(string[] args)
    {
        // string currentPath = Directory.GetCurrentDirectory();
        // string parentPath = Path.GetFullPath(Path.Combine(currentPath, @"..\.."));
        // string filePath = Path.GetFullPath(Path.Combine(parentPath, @"examples\temp\nested_data.bin"));

        // string filePath = @"C:\Users\ckasirer\repos\compas_pb\examples\temp\data_dict.bin";
        string filePath = @"C:\Users\weitingchen\project\compas_pb\examples\temp\example_dict.bin";

        // data.Data: AnyData
        // example #1: traverse without any abstraction, and no knowledge of the data structure

        byte[] byteData = File.ReadAllBytes(filePath);
        MessageData message = MessageData.Parser.ParseFrom(byteData);
        Console.WriteLine($"MessageData: {message.Data}");
        Console.WriteLine($"MessageData Type: {message.Data.GetType()}");

        // example #1.5: traverse without any abstraction, but with knowledge of the data structure
        AnyData data = message.Data;
        Console.WriteLine($"Data Type: {data.GetType()}");
        // have to checkt if the data is of a specific type before unpacking
        if (data.Data.Is(DictData.Descriptor))
        {
            var dictData = data.Data.Unpack<DictData>();
            Console.WriteLine($"DictData: {dictData}");
            foreach (var kvp in dictData.Data)
            {
                Console.WriteLine($"Key: {kvp.Key}, Value: {kvp.Value}");
            }
        }

        // example #2: traverse with abstraction, 1 level deep
        //      data: Dictionary<string, AnyData> -> TryGetValue<Dictionary<string, object>>(data) ?
        //      data: Dictionary<string, AnyData> -> TryGetValue<LineData>(data) ?
        //      data: Dictionary<string, AnyData> -> TryGetValue<List<object>>(data) ?

        // var data = DataHandler.PBLoad(filePath);
        // Console.WriteLine(data.GetType());
        // var dict = DataProcessor.TryGetValue<DictData>(data);
        // Console.WriteLine($"Dict :{dict}");

        // var point = DataProcessor.TryGetValue<PointData>(data);
        // Console.WriteLine($"Point: {point}");

        // var point = TryGetValue<Point>(data);
        // var dict = TryGetValue<Dict<string, object>>(data);
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
// }
