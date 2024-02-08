<script setup lang="ts">

const { status, data: token , signIn, signOut  } = await useAuth()

const loggedIn = computed(() => status.value === 'authenticated')

const protectedResponse = ref('')

const publicResponse = ref('')

async function login() {
  //const signInOptions = {callbackUrl: "http://localhost:9000", redirect: true, external: true}
  const signInOptions = {redirect: true, external: false}
  
  await signIn('keycloak', signInOptions)
}

async function logout() {
  await signOut()
}

const headers = useRequestHeaders(['cookie']) as HeadersInit

async function call_protected() {
  let accessToken = ""
  if(token.value) {
    accessToken = token.value["accessToken"];
  }

  const headers = {'authorization': `Bearer ${accessToken}` }
  
  const { error, data } = await useFetch('/litestar/protected', { headers: headers , 
  onResponseError({ request, response, options }) {
    console.log(response)
    protectedResponse.value =  String(response.status + " " + response.statusText + " " + response._data)  ;
  }});
  if(data.value) {
    console.log(data.value)
    protectedResponse.value =  String(data.value);
  }
  if(error.value) {
    console.log(error.value)
    protectedResponse.value =  String(error.value)  ;
  }
}

async function api_public() {
  const { data } = await useFetch('/litestar/public')
  console.log(data.value)
  publicResponse.value =  String(data.value);
}

</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 1em;
  background-color: #f4f4f4;
}
pre {
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  padding: 0em;
  overflow: auto;
  white-space: pre-wrap;  
  word-wrap: break-word; 
  width:70vw
}

.grid{
  display: grid;grid-template-columns: 1fr 4fr;gap: 2rem;
}
h1 {
  margin-bottom: 1em;
}
button {
  padding: 0.5em 0.5em;
  width: 10rem;
}
</style>
<template>
  

  <div  style="margin: 3rem;">
    <h1>Minimal example keycloak / JWT login</h1>

    <div class="grid">

      <span>Login</span>

      <div>
        <button v-if="loggedIn" @click="logout" :disabled="!loggedIn">Logout</button>
        <button v-else  @click="login" :disabled="loggedIn">Login</button>
      </div>

      <span>Status</span>
      <span>{{ status }}</span>

      <span>JWT Token</span>
      <pre>{{ token || 'no token present, are you logged in?'  }}{{  }}</pre>

      <span>
        <button  @click="api_public">Public API call</button>
      </span>
      <pre>{{ publicResponse }}</pre>

      <span><button  @click="call_protected">Protected API call</button></span>
      
      <pre> {{ protectedResponse }}</pre>
    </div>
  </div>
</template>
