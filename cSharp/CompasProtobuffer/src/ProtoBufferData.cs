using System;
using CompasPb.Data;
using Google.Protobuf;

// namespace CompasPb.Data.ProtoBufferData
// {
//     // Interface for Protocol Buffers conversion
//     public interface IProtoBufferConvertible<TProto>
//         where TProto : IMessage
//     {
//         TProto ToPb();
//     }

//     // Abstract Base class
//     public abstract class ProtoBufferData<T, TProto>
//         where T : class
//         where TProto : IMessage
//     {
//         protected T Obj { get; }

//         protected ProtoBufferData(T obj)
//         {
//             Obj = obj;
//         }

//         // Must implement this method by subclasses
//         public abstract TProto ToPb();
//     }

//     public class ProtoBufferPoint : ProtoBufferData<Dictionary<string, object>, PointData>, IProtoBufferConvertible<PointData>
//     {
//         public static AnyData.DataOneofCase Pbtype => AnyData.DataOneofCase.Point;

//         public ProtoBufferPoint(Dictionary<string, object> obj)
//             : base(obj) { }

//         public override PointData ToPb()
//         {
//             throw new NotImplementedException("ToPb method not implemented");
//         }

//         public static Dictionary<string, object> FromPb(IMessage protoData)
//         {
//             // Convert PointData to Dictionary<string, object>
//             Dictionary<string, object> pointDict = new Dictionary<string, object>();
//             if (protoData.Descriptor.Name == "PointData")
//             {
//                 PointData pointData = (PointData)protoData;
//                 pointDict["x"] = pointData.X;
//                 pointDict["y"] = pointData.Y;
//                 pointDict["z"] = pointData.Z;
//             }
//             return pointDict;
//         }
//     }

//     public class ProtoBufferAny : ProtoBufferData<object, AnyData>, IProtoBufferConvertible<AnyData>
//     {
//         public static AnyData.DataOneofCase PbType => AnyData.DataOneofCase.None;

//         private static readonly Dictionary<string, object> serializer = new Dictionary<string, object>() { { "Point", typeof(ProtoBufferPoint) } };

//         private static readonly Dictionary<string, object> deserializer;

//         // Constructor
//         static ProtoBufferAny()
//         {
//             deserializer = new Dictionary<string, object>();
//             foreach (var pair in serializer)
//             {
//                 string key = pair.Key.ToLower();
//                 deserializer[key] = pair.Value;
//             }
//         }

//         public ProtoBufferAny(object obj)
//             : base(obj) { }

//         public override AnyData ToPb()
//         {
//             throw new NotImplementedException("ToPb method not implemented");
//         }

//         public static object FromPb(AnyData protoData)
//         {
//             // Now I jsut retrun everything as Dictionary
//             AnyData.DataOneofCase type = protoData.DataCase;
//             try
//             {
//                 return protoData;
//             }
//             catch (Exception e)
//             {
//                 throw new InvalidOperationException($"Error deserializing ProtoData: {e.Message}", e);
//             }
//         }
//     }
// }
