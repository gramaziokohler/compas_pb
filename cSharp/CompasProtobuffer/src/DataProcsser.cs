using System;
using System.Collections.Generic;
using System.Linq;
using CompasPb.Data;
using Google.Protobuf.WellKnownTypes;

namespace CompassPb.Data
{
    public class DataProcessor
    {
        public static T TryGetValue<T>(AnyData data) where T: class, Google.Protobuf.IMessage, new()
        {
            try
            {
                if (data.Data.Is(new T().Descriptor))
                {
                    return data.Data.Unpack<T>();
                }
                else
                {
                    throw new InvalidCastException($"Cannot find {data.Data.GetType()} to {typeof(T)}");
                }
            }
            catch { }
            return default(T);
        }
    }

    /// <summary>
    /// Data Processor from object to protobuf messages.
    /// </summary>
    public class DataSerializer { }

    /// <summary>
    /// Data Processor from message to object.
    /// </summary>
    /// <summary>
    /// Data Processor from message to object.
    /// </summary>
    public class DataDeserializer
    {
        public T Deserialize<T>(AnyData data)
        {
            if (data == null)
            {
                throw new ArgumentNullException(nameof(data), "Data cannot be null");
            }
            if (data.Data == null)
            {
                return default(T);
            }
            try
            {
                if (data.Data.Is(DictData.Descriptor))
                {
                    var dictData = data.Data.Unpack<DictData>();
                    var deserializedDict = DeserializeMessageDict(dictData);
                    return (T)(object)deserializedDict;
                }
                else if (data.Data.Is(ListData.Descriptor))
                {
                    var listData = data.Data.Unpack<ListData>();
                    var deserializedList = DeserializeMessageList(listData);
                    return (T)(object)deserializedList;
                }
                else
                {
                    // Handle other message types
                    var deserializedValue = DeserializeAny(data);
                    return (T)(object)deserializedValue;
                }
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Failed to deserialize data to type {typeof(T)}", ex);
            }
        }

        private object DeserializeAny(AnyData anyData)
        {
            if (anyData?.Data == null)
            {
                return null;
            }

            if (anyData.Data.Is(DictData.Descriptor))
            {
                var dictData = anyData.Data.Unpack<DictData>();
                return DeserializeMessageDict(dictData);
            }
            else if (anyData.Data.Is(ListData.Descriptor))
            {
                var listData = anyData.Data.Unpack<ListData>();
                return DeserializeMessageList(listData);
            }
            // should be move to other class
            else if (anyData.Data.Is(PointData.Descriptor))
            {
                var pointData = anyData.Data.Unpack<PointData>();
                return new Dictionary<string, object>
                {
                    ["x"] = pointData.X,
                    ["y"] = pointData.Y,
                    ["z"] = pointData.Z
                };
            }
            else if (anyData.Data.Is(LineData.Descriptor))
            {
                var pointData = anyData.Data.Unpack<LineData>();
                return new Dictionary<string, object>
                {
                    ["start"] = pointData.Start,
                    ["end"] = pointData.End,
                };
            }
            else
            {
                return anyData.Data;
            }
        }

        private Dictionary<string, object> DeserializeMessageDict(DictData dataDict)
        {
            var result = new Dictionary<string, object>();
            if (dataDict?.Data == null)
            {
                return result;
            }
            foreach (var keyValuePair in dataDict.Data)
            {
                result[keyValuePair.Key] = DeserializeAny(keyValuePair.Value);
            }
            return result;
        }

        private List<object> DeserializeMessageList(ListData dataList)
        {
            var result = new List<object>();
            if (dataList?.Data == null)
            {
                return result;
            }
            foreach (var item in dataList.Data)
            {
                result.Add(DeserializeAny(item));
            }
            return result;
        }
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
//
//      data: Dictionary<string, AnyData> -> TryGetValue<Dictionary<string, object>>(data) ?
//      data: Dictionary<string, AnyData> -> TryGetValue<LineData>(data) ?
//      data: Dictionary<string, AnyData> -> TryGetValue<List<object>>(data) ?
//     }
// }

// class CompasPbApi
// {
//     public T TryGetValue<T>(AnyData obj)
//     {
//         throw new InvalidCastException($"Cannot cast {obj.GetType()} to {typeof(T)}");
//     }
// }
