# gRPC client to list routes of remote gobgp 

---
```
Language: Python / goRPC
Brief: Programattically get a list of routes from a gobgp process
Scope: 
Tags: 
State: 
Result: 
```
---

The gobgp daemon supports API access through gRPC client libraries. There is an example in the gobgp source using the gRPC client to add a router. I wanted to write a client to list the routes.

### Results

---

Works. 

Setting up an environment to write the script locally and communicate with a gobgp instance running in AWS was pretty straight forward. Built the python client code using the method in the gobgp documentation, opened up port 50051 on the EC2 instance and it just worked.

However this shows how little security there is in the API and another reason gobpg shouldn't be used anywhere near production.


### If I was to do more

---

Learn more about gRPC. The data types with protobuffs is pretty new to me. I faked my way through it but I would need to learn more.

Maybe make a pretty printer as an context to learn more about how gRPC works

### Notes

---

To generate documentation from gRPC proto files included with gobgp

`(base) [pickard@eris.local:] /tmp/gobgp-docs  % protoc --doc_out=. --doc_opt=html,index.html --proto_path=/Users/pickard/projects/3rdsrc/gobgp/api/ /Users/pickard/projects/3rdsrc/gobgp/api/*.proto`

To generate python gRPC interface for gobgp protos

`python -m grpc_tools.protoc -I/Users/pickard/projects/3rdsrc/gobgp/api/ --python_out=. --grpc_python_out=. /Users/pickard/projects/3rdsrc/gobgp/api/*.proto`


### Example 

---

```
/Users/pickard/projects/100_days_of_code_2022/local/py3_venv/bin/python /Users/pickard/projects/100_days_of_code_2022/day_29/list_path.py
destination {
  prefix: "10.0.0.0/24"
  paths {
    nlri {
      [type.googleapis.com/apipb.IPAddressPrefix] {
        prefix_len: 24
        prefix: "10.0.0.0"
      }
    }
    pattrs {
      [type.googleapis.com/apipb.OriginAttribute] {
        origin: 2
      }
    }
    pattrs {
      [type.googleapis.com/apipb.AsPathAttribute] {
        segments {
          type: AS_SEQUENCE
          numbers: 100
          numbers: 200
        }
      }
    }
    pattrs {
      [type.googleapis.com/apipb.NextHopAttribute] {
        next_hop: "1.1.1.1"
      }
    }
    age {
      seconds: 1649172085
    }
    best: true
    validation {
    }
    family {
      afi: AFI_IP
      safi: SAFI_UNICAST
    }
    source_id: "<nil>"
    neighbor_ip: "<nil>"
    local_identifier: 1
  }
}

destination {
  prefix: "11.0.0.0/24"
  paths {
    nlri {
      [type.googleapis.com/apipb.IPAddressPrefix] {
        prefix_len: 24
        prefix: "11.0.0.0"
      }
    }
    pattrs {
      [type.googleapis.com/apipb.OriginAttribute] {
        origin: 2
      }
    }
    pattrs {
      [type.googleapis.com/apipb.AsPathAttribute] {
        segments {
          type: AS_SEQUENCE
          numbers: 100
          numbers: 200
        }
      }
    }
    pattrs {
      [type.googleapis.com/apipb.NextHopAttribute] {
        next_hop: "1.1.1.1"
      }
    }
    age {
      seconds: 1649172806
    }
    best: true
    validation {
    }
    family {
      afi: AFI_IP
      safi: SAFI_UNICAST
    }
    source_id: "<nil>"
    neighbor_ip: "<nil>"
    local_identifier: 1
  }
}

destination {
  prefix: "12.0.0.0/24"
  paths {
    nlri {
      [type.googleapis.com/apipb.IPAddressPrefix] {
        prefix_len: 24
        prefix: "12.0.0.0"
      }
    }
    pattrs {
      [type.googleapis.com/apipb.OriginAttribute] {
        origin: 2
      }
    }
    pattrs {
      [type.googleapis.com/apipb.AsPathAttribute] {
        segments {
          type: AS_SEQUENCE
          numbers: 100
          numbers: 200
        }
      }
    }
    pattrs {
      [type.googleapis.com/apipb.NextHopAttribute] {
        next_hop: "1.1.1.1"
      }
    }
    age {
      seconds: 1649173140
    }
    best: true
    validation {
    }
    family {
      afi: AFI_IP
      safi: SAFI_UNICAST
    }
    source_id: "<nil>"
    neighbor_ip: "<nil>"
    local_identifier: 1
  }
}


Process finished with exit code 0
```