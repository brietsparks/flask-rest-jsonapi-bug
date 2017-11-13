## Setup

1. Clone repo
2. Checkout branch `with-0.12.6` and install Python dependencies
4. Start app and hit API path `/persons?include=events`
5. See correct response
6. Checkout branch `with-0.13.0` and install Python dependencies
7. Start app and hit API path `/persons?include=events`
8. See broken response

## Explanation

0.13.0 intruduced a bug where including a relationship on a collection causes resources without items of that relation to not be returned.

This project takes the [readme example](https://github.com/miLibris/flask-rest-jsonapi#a-minimal-api), adds an `event`
resource, and creates a many-to-many relation between it and the person resource.

A GET request to `/persons?include=events` will return the correct response for 0.12.6 and a broken one for 0.13.0.

With 0.12.6:

```
{
   data:[
      {
         type:"person",
         relationships:{
            events:{
               links:{
                  self:"/persons/1/relationships/events",
                  related:"/events?id=1"
               },
               data:[ ]
            }
         },
         attributes:{
            name:"Bob"
         },
         id:"1",
         links:{
            self:"/persons/1"
         }
      }
   ],
   links:{
      self:"/persons?include=events"
   },
   meta:{
      count:1
   },
   jsonapi:{
      version:"1.0"
   }
}
```

With 0.13.0:
```
{
   data:[ ],
   links:{
      self:"/persons?include=events"
   },
   meta:{
      count:1
   },
   jsonapi:{
      version:"1.0"
   }
}
```
