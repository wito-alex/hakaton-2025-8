'use client';
import { Label } from "./ui/label";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useRef } from "react";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { hasCookie, setCookie } from "cookies-next";
import store from "@/store/authStore";
import { observer } from "mobx-react";

const Login = () => {
  const submitBtn = useRef(null);

  const submit = (e) => {
    e.preventDefault();
    submitBtn.current.click();
  }
  const authorization = (e) => {
    e.preventDefault();
    const data = {"username": e.target[0].value, "password": e.target[1].value}
       const formData = new FormData();
       formData.append("username", e.target[0].value);
       formData.append("password", e.target[1].value);

      fetch("http://45.144.179.106:8001/api/token/", {
        method: "POST",
        headers: {
          Accept: "application/json, text/plain, */*",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((res) => res.json())
        .then((res) => {
          setCookie('refresh', res.refresh);
          setCookie("access", res.access);
          store.setAuth(true);
  });
    }
  


  return (
    <div className="w-full h-screen flex items-center justify-center">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>Вход в систему</CardTitle>
          <CardDescription>
            Введите данные учетной записи для входа
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={authorization}>
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-2">
                <Label htmlFor="login">Логин</Label>
                <Input type="text" id="login" required />
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="password">Пароль</Label>
                <Input type="password" id="password" required />
              </div>
            </div>
            <button className="hidden" ref={submitBtn}></button>
          </form>
        </CardContent>
        <CardFooter className="flex-col gap-2">
          <Button className="w-full" onClick={submit}>
            Войти
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default observer(Login);

