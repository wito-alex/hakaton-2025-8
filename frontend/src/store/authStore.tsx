import {observable} from 'mobx';

const store = observable({
  auth: false,
  setAuth(auth:boolean) {
    this.auth = auth;
  }
})

export default store;