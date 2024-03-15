## About the UUIDs

At some point I had my own PHP code to generate GUIDs/UUIDs.

That code is lost until I reproduce it in a gist and therefore for today, fuck it.

As of 2024 I'm using all-new UUIDs generated from [UUID Tools](https://www.uuidtools.com/v5) - arbitrarily chosen via google.

No, the UUIDs are not cryptographically secure. I don't need them to be. Actually what I need is for them to be reproducible.

### Here's the reproducibility:

Namespace is generated from ns:DNS with danieljpost.pro as the DNS, producing [2d21c062-ad99-5909-a8f9-ca62f3f2901c](https://www.uuidtools.com/api/generate/v5/namespace/ns:dns/name/base64:ZGFuaWVsanBvc3QucHJv) or [same result](https://www.uuidtools.com/api/generate/v5/namespace/ns:dns/name/danieljpost.pro)

All other UUIDs follow one of several rules:

1) skills.id: UUID is skillname converted to v5 with my namespace [skillname](https://www.uuidtools.com/api/generate/v5/namespace/2d21c062-ad99-5909-a8f9-ca62f3f2901c/name/base64:c2tpbGxuYW1l) ie [skillname](https://www.uuidtools.com/api/generate/v5/namespace/2d21c062-ad99-5909-a8f9-ca62f3f2901c/name/skillname) 
1) company.id: UUID is company url converted to v5 with my namespace i.e. [company.url](https://www.uuidtools.com/api/generate/v5/namespace/2d21c062-ad99-5909-a8f9-ca62f3f2901c/name/base64:Y29tcGFueS51cmw=) or [company.url](https://www.uuidtools.com/api/generate/v5/namespace/2d21c062-ad99-5909-a8f9-ca62f3f2901c/name/company.url)
1) gig.id: Eff it. Just a short name, for now. TODO: 


At some point soon enough I'll reproduce the APIs above in JavaScript in a [CodeSandbox](fixme)