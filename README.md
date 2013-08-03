# Field Marshal

Easy marshaling, based on Golang structs

## Example

These resources are based on resources from the [Docker REST API][docker].

```python
import fieldmarshal


class NetworkSettings(fieldmarshal.Struct):
    ip_address    = str
    ip_prefix_len = int
    gateway       = str
    bridge        = str


class Container(fieldmarshal.Struct):
    network_settings = NetworkSettings
    id              = str
    image           = str


container = Container(id="foo")

print container.id
# "foo"

print container.image
# ""

print fieldmarshal.dumps(Container)
# {
#   "network_settings": {
#      "ip_address": "",
#      "ip_prefix_len": 0,
#      "gateway": "",
#      "bridge": ""
#   },
#   "id": "foo",
#   "image": ""
# }
```

[docker]: http://docs.docker.io/en/latest/api/docker_remote_api_v1.4/#id7
