"use client";

import { FolderUp, BadgeCheck, BadgeInfo } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Separator } from "@/components/ui/separator";
import { useRef } from "react";
import CircularProgress from "@/components/ui/circular-progress";

import { DatePickerRu } from "@/components/ui/date-picker-ru";

import { toast } from "sonner";
import store from "@/store/loadStore";
import { observer } from "mobx-react";
import SparkMD5 from "spark-md5";
import { getCookie } from "cookies-next";
import {
  CHUNK_SIZE,
  UPLOAD_URL,
  TOKEN_URL,
  TOKEN_REFRESH_URL,
} from "@/constants/upload";
const ImageLoader = () => {
  const filePicker = useRef(null);
  const [selectedFile, setSelectedFile] = useState(false);
  const [loading, setLoading] = useState(true);

  const [drag, setDrag] = useState(false);
  const [selectedGender, setSelectedGender] = useState("male");

  const [access, setAccess] = useState(getCookie("access"));
  const [refresh, setRefresh] = useState(getCookie("refresh"));

  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const onDialogClose = () => {
    setLoading(false);
    setSelectedFile(false);
    setIsDialogOpen(false);
  };

  //let controller = new AbortController();

  function dragStartHandler(e) {
    e.preventDefault();
    setDrag(true);
  }

  function dragLeaveHandler(e) {
    e.preventDefault();
    setDrag(false);
  }

  function parseJwt(token: any) {
    try {
      return JSON.parse(atob(token.split(".")[1]));
    } catch (e) {
      return null;
    }
  }

  async function getValidAccessToken() {
    if (!access) return null;

    const decodedToken = parseJwt(access);
    const isExpired = decodedToken && decodedToken.exp * 1000 < Date.now();

    if (!isExpired) {
      return access;
    }

    //toast.warning("Токен доступа истек, идет обновление...")

    try {
      const response = await fetch(TOKEN_REFRESH_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refresh }),
      });
      if (!response.ok) throw new Error("Ошибка обновления токена");

      const data = await response.json();
      setAccess(data.access);
      //toast.success("Токен успешно обновлен!")
      return data.access;
    } catch (error) {
      setAccess(getCookie("access"));
      setRefresh(getCookie("refresh"));
      setLoading(false);
      setSelectedFile(false);
      toast.error("Сессия истекла, требуется повторная авторизация", {
        style: {
          backgroundColor: "rgba(193, 0, 7, 0.48)",
          borderColor: "#c10007",
        },
      });
      return null;
    }
  }

  const calculateMD5 = (file, callback) => {
    const blobSlice = File.prototype.slice;
    const chunks = Math.ceil(file.size / CHUNK_SIZE);
    let currentChunk = 0;
    const spark = new SparkMD5.ArrayBuffer();
    const fileReader = new FileReader();

    fileReader.onload = (e) => {
      spark.append(e.target.result);
      currentChunk++;
      const percent = Math.round((currentChunk / chunks) * 100);
      store.setMessage("Расчет MD5");
      store.setPercent(percent);
      if (currentChunk < chunks) {
        loadNextChunk();
      } else {
        callback(spark.end());
      }
    };
    fileReader.onerror = () => {
      setLoading(false);
      setSelectedFile(false);
      toast.error("Ошибка расчета MD5", {
        style: {
          backgroundColor: "rgba(193, 0, 7, 0.48)",
          borderColor: "#c10007",
        },
      });
    };
    const loadNextChunk = () => {
      const start = currentChunk * CHUNK_SIZE;
      const end = Math.min(start + CHUNK_SIZE, file.size);
      fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
    };
    loadNextChunk();
  };

  async function startUpload(file, md5) {
    const totalSize = file.size;
    let start = 0;
    let uploadUrl = UPLOAD_URL;

    try {
      while (start < totalSize) {
        const end = Math.min(start + CHUNK_SIZE, totalSize);
        const chunk = file.slice(start, end);
        const contentRange = `bytes ${start}-${end - 1}/${totalSize}`;

        const percent = Math.round((end / totalSize) * 100);
        store.setPercent(percent);
        store.setMessage("Загружается...");

        const formData = new FormData();
        formData.append("file", chunk);
        formData.append("filename", file.name);

        const currentAccessToken = await getValidAccessToken();
        if (!currentAccessToken) throw new Error("Session expired.");

        const chunkResponse = await fetch(uploadUrl, {
          method: "PUT",
          headers: {
            "Content-Range": contentRange,
            Authorization: `Bearer ${currentAccessToken}`,
          },
          body: formData,
          //signal: controller.signal,
        });

        if (!chunkResponse.ok) {
          const errorData = await chunkResponse.json();
          setLoading(false);
          setSelectedFile(false);
          toast.error(`Ошибка загрузки: ${JSON.stringify(errorData)}`, {
            className: "bg-red-200 border-red-500",
            style: {
              backgroundColor: "rgba(193, 0, 7, 0.48)",
              borderColor: "#c10007",
            },
          });
          throw new Error(`Chunk upload failed: ${JSON.stringify(errorData)}`);
        }

        const responseData = await chunkResponse.json();
        uploadUrl = responseData.url;
        start = end;
      }

      store.setMessage("Завершение загрузки...");

      const finalAccessToken = await getValidAccessToken();
      if (!finalAccessToken) throw new Error("Session expired.");

      const finalResponse = await fetch(uploadUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${finalAccessToken}`,
        },
        body: JSON.stringify({ md5: md5 }),
        //signal: controller.signal,
      });

      if (!finalResponse.ok) {
        const errorData = await finalResponse.json();
        setLoading(false);
        throw new Error(`Finalization failed: ${JSON.stringify(errorData)}`);
      }
      store.setMessage("Загрузка завершена!");
      setLoading(false);
    } catch (error) {
      if (error.name == "AbortError") {
        // обработать ошибку от вызова abort()
        alert("Прервано!");
      } else {
        store.setMessage(`Error: ${error.message}`);
        store.setPercent(0);
        console.error("Upload failed:", error);
      }
    }
  }

  async function onDropHandler(e) {
    e.preventDefault();
    const validToken = await getValidAccessToken();
    if (!validToken) {
      setLoading(false);
      setSelectedFile(false);
      toast.error("Требуется повторная авторизация", {
        style: {
          backgroundColor: "rgba(193, 0, 7, 0.48)",
          borderColor: "#c10007",
        },
      });
      return;
    }
    let files = [...e.dataTransfer.files];

    setDrag(false);
    setSelectedFile(files[0]);
    setLoading(true);
    store.setMessage("Обработка...");

    calculateMD5(files[0], (md5) => {
      store.setMessage(`MD5: ${md5}. Загружается...`);
      startUpload(files[0], md5);
    });
  }

  async function handleChange(event) {
    setSelectedFile(event.target.files[0]);
    const validToken = await getValidAccessToken();
    if (!validToken) {
      setLoading(false);
      setSelectedFile(false);
      toast.error("Требуется повторная авторизация", {
        style: {
          backgroundColor: "rgba(193, 0, 7, 0.48)",
          borderColor: "#c10007",
        },
      });
      return;
    }
    setLoading(true);
    store.setMessage("Обработка...");

    calculateMD5(event.target.files[0], (md5) => {
      store.setMessage(`MD5: ${md5}. Загружается...`);
      startUpload(event.target.files[0], md5);
    });
  }

  const handlePick = () => {
    filePicker.current.click();
  };

  const handleOpenChange = (open: boolean) => {
    if (!open) {
      // Вызываем нашу функцию
      onDialogClose();
    }

    // Не забываем обновить состояние, чтобы диалог мог открываться и закрываться
    setIsDialogOpen(open);
  };

  return (
    <div className="my-4 flex flex-row gap-4 items-center">
      <Dialog open={isDialogOpen} onOpenChange={handleOpenChange}>
        <form>
          <DialogTrigger asChild>
            <Button variant="outline" className="hover:cursor-pointer">
              Добавить исследование
            </Button>
          </DialogTrigger>
          <DialogContent className="min-w-[80vw]">
            <DialogHeader>
              <DialogTitle>
                Добавить исследование
              </DialogTitle>
              <DialogDescription>
                Информация о пациенте пока не обрабатывается
              </DialogDescription>
              <Separator className="mt-2" />
            </DialogHeader>
            {/* {!selectedFile && (
                <div
                  className={`rounded-md p-4 flex flex-col items-center gap-4 border border-dashed border-white ${
                    drag ? "bg-slate-300" : ""
                  }`}
                  onDragStart={(e) => dragStartHandler(e)}
                  onDragLeave={(e) => dragLeaveHandler(e)}
                  onDragOver={(e) => dragStartHandler(e)}
                >
                  <FolderUp className="" width={40} height={40} />
                  <p className="">Перетащите архив чтобы начать загрузку</p>
                  <p className="">ИЛИ</p>
                  <Button
                    variant="outline"
                    className="hover:cursor-pointer"
                    onClick={handlePick}
                  >
                    Выбрать архив
                  </Button>
                  <input
                    className="hidden"
                    type="file"
                    //multiple
                    //accept="image/*, png, jpg, gif, web,"
                    accept=".zip"
                    onChange={handleChange}
                    ref={filePicker}
                  />
                </div>
              )}
              {selectedFile && (
                <div
                  className="rounded-md flex flex-col items-center gap-4 border border-white"
                  onDragStart={(e) => dragStartHandler(e)}
                  onDragLeave={(e) => dragLeaveHandler(e)}
                  onDragOver={(e) => dragStartHandler(e)}
                  onDrop={(e) => onDropHandler(e)}
                >
                  <CircularProgress progress={100} color="green" />
                  <p className="">Загружается...</p>
                  <Button variant="outline" className="hover:cursor-pointer">
                    Отменить
                  </Button>
                </div>
              )} */}
            <div className="flex flex-row justify-between items-center w-full">
              <div className="w-[48%]">
                <div className="flex flex-col gap-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="flex flex-col gap-2">
                      <Label htmlFor="policy">Полис</Label>
                      <Input
                        type="text"
                        id="policy"
                        placeholder="0000 0000 0000 0000"
                      />
                    </div>
                    <div className="flex flex-col gap-2">
                      <Label htmlFor="policy">Фамилия</Label>
                      <Input type="text" id="policy" placeholder="Иванов" />
                    </div>
                    <div className="flex flex-col gap-2">
                      <Label htmlFor="name">Имя</Label>
                      <Input type="text" id="name" placeholder="Иван" />
                    </div>
                    <div className="flex flex-col gap-2">
                      <Label htmlFor="policy">Отчество</Label>
                      <Input type="text" id="policy" placeholder="Иванович" />
                    </div>
                    <div className="flex flex-col gap-2">
                      <Label htmlFor="name">Пол</Label>
                      <Select
                        value={selectedGender}
                        onValueChange={(value) => {
                          setSelectedGender(value);
                        }}
                      >
                        <SelectTrigger className="flex-1 w-full">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectGroup>
                            <SelectItem value="male">Мужской</SelectItem>
                            <SelectItem value="female">Женский</SelectItem>
                          </SelectGroup>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="flex flex-col gap-2">
                      <Label htmlFor="policy">Дата рождения</Label>
                      <DatePickerRu />
                    </div>
                  </div>
                  <div className="flex flex-row gap-4"></div>
                  <div className="flex flex-row gap-4"></div>
                </div>
              </div>
              <Separator orientation="vertical" className="text-gray-900" />
              <div className="w-[48%]">
                {!selectedFile && (
                  <div
                    className={`h-48 rounded-md p-4 flex flex-col items-center justify-center gap-4 border border-dashed border-white ${
                      drag ? "bg-secondary" : ""
                    }`}
                    onDragStart={(e) => dragStartHandler(e)}
                    onDragLeave={(e) => dragLeaveHandler(e)}
                    onDragOver={(e) => dragStartHandler(e)}
                    onDrop={(e) => onDropHandler(e)}
                  >
                    <FolderUp className="" width={40} height={40} />
                    <p className="">
                      Перетащите .zip архив чтобы начать загрузку
                    </p>
                    <Button
                      variant="outline"
                      className="hover:cursor-pointer"
                      onClick={handlePick}
                    >
                      Выбрать архив
                    </Button>
                    <input
                      className="hidden"
                      type="file"
                      //multiple
                      //accept="image/*, png, jpg, gif, web,"
                      accept=".zip"
                      onChange={handleChange}
                      ref={filePicker}
                    />
                  </div>
                )}
                {selectedFile && (
                  <div
                    className="h-48 rounded-md flex flex-col items-center justify-center gap-4 border border-white"
                    onDragStart={(e) => dragStartHandler(e)}
                    onDragLeave={(e) => dragLeaveHandler(e)}
                    onDragOver={(e) => dragStartHandler(e)}
                    onDrop={(e) => onDropHandler(e)}
                  >
                    {loading && (
                      <CircularProgress
                        progress={store.percent}
                        color="#aae7fd"
                      />
                    )}
                    {!loading && (
                      <BadgeCheck
                        width={60}
                        height={60}
                        className="text-lime-600"
                      />
                    )}

                    <p className="">{store.message}</p>
                    {/* {loading && (
                      <Button
                        variant="outline"
                        className="hover:cursor-pointer"
                        onClick={() => controller.abort()}
                      >
                        Отменить
                      </Button>
                    )} */}
                  </div>
                )}
              </div>
            </div>
            <Separator />
            <DialogFooter>
              <Button variant="outline" onClick={onDialogClose}>
                Отмена
              </Button>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button onClick={onDialogClose}>Добавить исследование</Button>
                </TooltipTrigger>
                <TooltipContent className="bg-card flex gap-2">
                  <BadgeInfo className="text-card-foreground mt-1.5"/>
                  <div className="flex flex-col gap-1">
                    <p className="font-semibold text-card-foreground w-72">
                      Сохранение и использование данных о пациенте находится в
                      процессе реализации
                    </p>
                    <p className="text-card-foreground w-72 mb-2">
                      .zip исследование уже обрабатывается
                    </p>
                  </div>
                </TooltipContent>
              </Tooltip>
            </DialogFooter>
          </DialogContent>
        </form>
      </Dialog>
    </div>
  );
};

export default observer(ImageLoader);
