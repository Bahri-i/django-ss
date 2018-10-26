import { OrderEvents } from "../types/globalTypes";
import { Home } from "./types/home";

export const shop: (placeholderImage: string) => Home = (
  placeholderImage: string
) => ({
  activities: {
    __typename: "OrderEventCountableConnection",
    edges: [
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-09-14T16:10:27.137126+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDoxOA==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED_FROM_DRAFT,
          user: {
            __typename: "User",
            email: "admin@example.com",
            id: "VXNlcjoyMQ=="
          }
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-03T13:28:46.325279+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDozNQ==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED,
          user: null
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-03T13:29:01.837496+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDozNw==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.ORDER_FULLY_PAID,
          user: null
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-04T01:01:51.243723+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo1OA==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED_FROM_DRAFT,
          user: {
            __typename: "User",
            email: "admin@example.com",
            id: "VXNlcjoyMQ=="
          }
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-04T19:36:18.831561+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo2Nw==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED_FROM_DRAFT,
          user: {
            __typename: "User",
            email: "admin@example.com",
            id: "VXNlcjoyMQ=="
          }
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-04T19:38:01.420365+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo2OA==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED_FROM_DRAFT,
          user: {
            __typename: "User",
            email: "admin@example.com",
            id: "VXNlcjoyMQ=="
          }
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-05T12:30:57.268592+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo3MQ==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED_FROM_DRAFT,
          user: {
            __typename: "User",
            email: "admin@example.com",
            id: "VXNlcjoyMQ=="
          }
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-08T09:50:42.622253+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo3Mw==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED,
          user: null
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-12T15:51:11.665838+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo3Nw==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED_FROM_DRAFT,
          user: {
            __typename: "User",
            email: "admin@example.com",
            id: "VXNlcjoyMQ=="
          }
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-25T11:25:58.843860+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo3OA==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED,
          user: null
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-26T09:34:57.580167+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo4MA==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.PLACED,
          user: null
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-26T09:38:02.440061+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo4Mg==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.ORDER_FULLY_PAID,
          user: null
        }
      },
      {
        __typename: "OrderEventCountableEdge",
        node: {
          __typename: "OrderEvent",
          amount: null,
          composedId: null,
          date: "2018-10-26T09:38:02.467443+00:00",
          email: null,
          emailType: null,
          id: "T3JkZXJFdmVudDo4NA==",
          message: null,
          oversoldItems: null,
          quantity: null,
          type: OrderEvents.ORDER_FULLY_PAID,
          user: null
        }
      }
    ]
  },
  ordersToCapture: {
    __typename: "OrderCountableConnection",
    totalCount: 0
  },
  ordersToFulfill: {
    __typename: "OrderCountableConnection",
    totalCount: 1
  },
  ordersToday: {
    __typename: "OrderCountableConnection",
    totalCount: 1
  },
  productTopToday: {
    __typename: "ProductVariantCountableConnection",
    edges: [
      {
        __typename: "ProductVariantCountableEdge",
        node: {
          __typename: "ProductVariant",
          attributes: [
            {
              __typename: "SelectedAttribute",
              value: {
                __typename: "AttributeValue",
                id: "QXR0cmlidXRlVmFsdWU6OTI=",
                name: "XS",
                sortOrder: 0
              }
            }
          ],
          id: "UHJvZHVjdFZhcmlhbnQ6NDM=",
          product: {
            __typename: "Product",
            id: "UHJvZHVjdDo4",
            name: "Gardner-Martin",
            price: {
              __typename: "Money",
              amount: 37.65,
              currency: "USD"
            },
            thumbnailUrl: placeholderImage
          },
          quantityOrdered: 1,
          revenue: {
            __typename: "TaxedMoney",
            gross: {
              __typename: "Money",
              amount: 37.65,
              currency: "USD"
            }
          }
        }
      }
    ]
  },
  productsOutOfStock: {
    __typename: "ProductCountableConnection",
    totalCount: 0
  },
  salesToday: {
    __typename: "TaxedMoney",
    gross: {
      __typename: "Money",
      amount: 57.15,
      currency: "USD"
    }
  }
});
