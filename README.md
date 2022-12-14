
# Stock and Crypto API with Profilio Manager

With this API users can retrieve Stock and Crypto Data. They can also register then create and manage their portfolio.




## API Reference

#### Get Stock Data

```http
  GET /stock/<string:symbol>
```

| Parameter | Type     | Description                | Example                |
| :-------- | :------- | :------------------------- | :------------------------- |
| `symbol` | `string` | Enter stock symbol to get data | /stock/aapl |

#### Get Crypto Data

```http
  GET /crypto/<string:name>
```

| Parameter | Type     | Description                | Example                |
| :-------- | :------- | :------------------------- | :------------------------- |
| `name` | `string` | Enter crypto name to get data | /crypto/bitcoin |

#### Register User

```http
  POST /register
```

| Type     | Description                | Example                |
| :------- | :------------------------- | :------------------------- |
| `raw JSON` | Register User | {"username":"john123","password":"password"} |

#### Login User

###### The user will recieve an access token to enter in header as a Bearer Token

```http
  POST /login
```
| Type     | Description                | Example                |
| :------- | :------------------------- | :------------------------- |
| `raw JSON` | Login User | {"username":"john123","password":"password"} |

#### Delete User

```http
  DEL /deleteuser
```

| Type     | Description                | Example                |
| :------- | :------------------------- | :------------------------- |
| `raw JSON` | Delete User | {"username":"john123","password":"password"} |

#### Add Asset to Profilio

```http
  POST /adjustasset
```

| Type     | Description                | Example                |
| :------- | :------------------------- | :------------------------- |
| `raw JSON` | Create Asset | {"name":"aapl","quantity":"3","type":"stock"} |

#### Adjust Asset in Profilio

```http
  PATCH /adjustasset
```

| Type     | Description                | Example                |
| :------- | :------------------------- | :------------------------- |
| `raw JSON` | Adjust Asset | {"name":"aapl","quantity":"2","type":"stock"} |



#### Delete Asset from Profilio

```http
  DEL /adjustasset
```

| Type     | Description                | Example                |
| :------- | :------------------------- | :------------------------- |
| `raw JSON` | Delete Asset | {"name":"aapl","type":"stock"} |

#### View Portfolio


```http
  GET /portfolio
```

| Parameter | Description                |
| :-------- | :------------------------- |
| `none`  | Returns assets in profilio with value of each asset |

#### View Profilio Balance


```http
  GET /balance
```

| Parameter | Description                |
| :-------- | :------------------------- |
| `none`  | Returns profilio balance |
