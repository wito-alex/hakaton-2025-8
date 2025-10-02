import { observable } from "mobx";

const store = observable({
  message: "",
  percent: 0,
  setMessage(message: string) {
    this.message = message;
  },
  setPercent(percent: number) {
    this.percent = percent;
  },
});

export default store;
