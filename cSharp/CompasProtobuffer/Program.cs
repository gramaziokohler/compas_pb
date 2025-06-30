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
        byte[] byteData = File.ReadAllBytes(filePath);

        // example #1: traverse without any abstraction, and no knowledge of the data structure
        Console.WriteLine("##########");
        Console.WriteLine("Example #1: Traverse without any abstraction, and no knowledge of the data structure");
        Console.WriteLine("##########");
        MessageData message = MessageData.Parser.ParseFrom(byteData);
        // message AnyData
        Console.WriteLine($"MessageData Type: {message.Data.GetType()}\n");
        if (message.Data is AnyData)
        {
            var data = message.Data.Data;
            if (data.Is(DictData.Descriptor))
            {
                var dictData = data.Unpack<DictData>();
                Console.WriteLine($"DictData: {dictData}\n");
                foreach (var kvp in dictData.Data)

                {
                    Console.WriteLine(kvp.Value.Data);
                    var innerData = kvp.Value.Data;
                    if (innerData.Is(ListData.Descriptor))
                    {
                        var list = innerData.Unpack<ListData>();
                        Console.WriteLine($"listData: {list}");
                    }
                    else
                    {
                        Console.WriteLine("Unknown data type in DictData value");
                    }
                }
            }
            // maybe we hvae to check all the data....
        }
        else
        {
            Console.WriteLine("data is not AnyData");
        }

        // example #1.5: traverse without any abstraction, but with knowledge of the data structure
        Console.WriteLine();
        Console.WriteLine("##########");
        Console.WriteLine("Example #1.5: Traverse without any abstraction, but with knowledge of the data structure");
        Console.WriteLine("##########");

        AnyData inputAnyData = message.Data;
        Console.WriteLine($"Input AnyData Type: {inputAnyData.GetType()}");
        // have to check if the data is of a specific type before unpacking
        if (inputAnyData.Data.Is(DictData.Descriptor))
        {
            var dictData = inputAnyData.Data.Unpack<DictData>();
            Console.WriteLine($"DictData: {dictData}");
            foreach (var kvp in dictData.Data)
            {
                // Console.WriteLine($"Key: {kvp.Key}, Value Type: {kvp.Value.Data.GetType()}");
                if (kvp.Value.Data.Is(ListData.Descriptor))
                {
                    var listData = kvp.Value.Data.Unpack<ListData>();
                    // Console.WriteLine($"ListData: {listData}");
                    foreach (var item in listData.Data)
                    {
                        // unpack the item data as WellKonwnTypes.Any
                        Console.WriteLine($"Item Type: {item.Data.GetType()}");
                        item.Data.TryUnpack<PointData>(out PointData point);
                        item.Data.TryUnpack<FrameData>(out FrameData frame);
                        item.Data.TryUnpack<VectorData>(out VectorData vector);
                        if (point != null)
                        {
                            Console.WriteLine($"Point: {point.X:F2}, {point.Y:F2}, {point.Z:F2}");
                        }
                        else if (frame != null)
                        {
                            Console.WriteLine($"frame: point: {frame.Point.X:F2}, {frame.Point.Y:F2}, {frame.Point.Z:F2}, " +
                                              $"xAxis: {frame.Xaxis.X:F2}, {frame.Xaxis.Y:F2}, {frame.Xaxis.Z:F2}, " +
                                              $"yAxis: {frame.Yaxis.X:F2}, {frame.Yaxis.Y:F2}, {frame.Yaxis.Z:F2}");
                        }
                        else if (vector != null)
                        {
                            Console.WriteLine($"Vector: {vector.X:F2}, {vector.Y:F2}, {vector.Z:F2}");
                        }
                        else
                        {
                            Console.WriteLine("Unknown data type in ListData item");
                        }
                    }
                }
                else
                {
                    Console.WriteLine("Unknown data type in DictData value");
                }
            }
        }
        else
        {
            Console.WriteLine("Input AnyData is not DictData");
        }

        // example #2: traverse with abstraction, 1 level deep
        Console.WriteLine();
        Console.WriteLine("##########");
        Console.WriteLine("Example #1.5: Traverse without any abstraction, but with knowledge of the data structure");
        Console.WriteLine("##########");

        // var data = DataHandler.PBLoad(filePath);
        // Console.WriteLine(data.GetType());
        var dictonary = DataProcessor.TryGetValue<DictData>(inputAnyData);
        Console.WriteLine($"Dict :{dictonary}");

        // var pt = DataProcessor.TryGetValue<PointData>(inputAnyData);
        // Console.WriteLine($"Point: {pt}");

        // var point = TryGetValue<Point>(data);
        // var dict = TryGetValue<Dict<string, object>>(data);
    }
}
