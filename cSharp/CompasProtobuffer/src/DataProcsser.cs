using System;
using System.Collections.Generic;
using System.Linq;
using CompasPb.Data;

namespace CompasPb.Data
{
    public class DataProcesser
    {
        public static T TryGetValue<T>(MessageData obj)
        {
            Console.WriteLine($"Trying to get value of type {typeof(T)} from {obj.GetType()}");
            return (T)(object)obj;
        }
    }
}

// namespace CompasPb.Data.Processor
// {
//     /// <summary>
//     /// * Data Processor for object to protobuf messages.
//     /// </summary>
//     public class DataSerializer { }

//     /// <summary>
//     /// * Data Decoder for protobuf messages to csharp object.
//     /// </summary>
//     public class DataDeserializer
//     {
//         private readonly byte[] _data;

//         public DataDeserializer(byte[] data)
//         {
//             if (data == null || data.Length == 0)
//             {
//                 throw new ArgumentException("Binary data is null or empty.");
//             }
//             _data = data;
//         }

//         /// <summary>
//         /// Deserializes a message from binary data into its corresponding object representation.
//         /// </summary>
//         /// <returns>
//         /// The deserialized object, which could be a dictionary, a list, or the original data type.
//         /// </returns>
//         /// <exception cref="ArgumentException">
//         /// Thrown when the binary data is null or empty.
//         /// </exception>
//         public object DeserializeMessage()
//         {
//             MessageData messageData = DeserializeMessageBts();
//             AnyData anyData = messageData.Data;
//             return DeserializeAny(anyData);
//         }

//         /// <summary>
//         /// Deserializes binary data into a <see cref="MessageData"/> object.
//         /// </summary>
//         /// <returns>
//         /// A <see cref="MessageData"/> object parsed from the binary data.
//         /// </returns>
//         /// <exception cref="ArgumentException">
//         /// Thrown when the binary data is null or empty.
//         /// </exception>
//         public MessageData DeserializeMessageBts()
//         {
//             if (_data == null || _data.Length == 0)
//             {
//                 throw new ArgumentException("Binary data is null or empty.");
//             }
//             return MessageData.Parser.ParseFrom(_data);
//         }

//         /// <summary>
//         /// Deserializes an object of type <see cref="AnyData"/> into its specific representation.
//         /// </summary>
//         /// <param name="data">The object to be deserialized, expected to be of type <see cref="AnyData"/>.</param>
//         /// <returns>
//         /// The deserialized object, which could be a dictionary, a list, or the original <see cref="AnyData"/> object.
//         /// </returns>
//         private object DeserializeAny(object data)
//         {
//             if (data.GetType() == typeof(AnyData))
//             {
//                 AnyData anyData = (AnyData)data;
//                 if (anyData.DataCase == AnyData.DataOneofCase.Dict && anyData.Dict != null)
//                 {
//                     return DeserializeMessageDict(anyData.Dict);
//                 }
//                 else if (anyData.DataCase == AnyData.DataOneofCase.List && anyData.List != null)
//                 {
//                     return DeserializeMessageList(anyData.List);
//                 }
//                 else
//                 {
//                     return ProtoBufferAny.FromPb(anyData);
//                 }
//             }
//             return data;
//         }

//         private Dictionary<string, object> DeserializeMessageDict(DictData dataDict)
//         {
//             Dictionary<string, object> dataOffset = new Dictionary<string, object>();

//             if (dataDict == null)
//             {
//                 return dataOffset;
//             }
//             foreach (var keyValPair in dataDict.Data)
//             {
//                 dataOffset[keyValPair.Key] = DeserializeAny(keyValPair.Value);
//             }
//             return dataOffset;
//         }

//         private List<object> DeserializeMessageList(ListData dataList)
//         {
//             List<object> dataOffset = new List<object>();
//             if (dataList == null)
//             {
//                 return dataOffset;
//             }
//             foreach (var item in dataList.Data)
//             {
//                 dataOffset.Add(DeserializeAny(item));
//             }
//             return dataOffset;
//         }
//     }
// }
