"use client"
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ExternalLink, Eye, Pause, Pen, Trash, FolderUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import {
  Calculator,
  Calendar,
  CreditCard,
  Settings,
  Smile,
  User,
} from "lucide-react";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command";
import { useState } from "react";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import { useRef } from "react";
import CircularProgress from "@/components/ui/circular-progress";
import DatePicker from "@/components/ui/date-picker";
import { DatePickerRu } from "@/components/ui/date-picker-ru";
import { DataTable } from "@/components/ui/data-table";

const items = ['one', 'two', 'three']

export default function Home() {
  const filePicker = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [drag, setDrag] = useState(false);
  const [selectedGender, setSelectedGender] = useState('male')

  function dragStartHandler(e) {
    e.preventDefault();
    console.log("занесли");
    setDrag(true);
  }

  function dragLeaveHandler(e) {
    e.preventDefault();
    console.log("вынесли");
    setDrag(false);
  }

  function onDropHandler(e) {
    e.preventDefault();

    console.log("отпустили");
    let files = [...e.dataTransfer.files];
    setDrag(false);
    setSelectedFile(files[0])
    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("userId", '1');
    //axios.post("url", formData, options);
    console.log(formData);
  }

  const handleChange = (event) => {
    console.log('handleChange')
    console.log(event.target.files);
    setSelectedFile(event.target.files[0]);
  };

  const handlePick = () => {
    filePicker.current.click();
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-row items-center gap-4">
        <Dialog>
          <form>
            <DialogTrigger asChild>
              <Button variant="outline">Добавить исследование</Button>
            </DialogTrigger>
            <DialogContent className="min-w-[80vw]">
              <DialogHeader>
                <DialogTitle>Добавить исследование</DialogTitle>
                <Separator />
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
              <div className="flex flex-row justify-between w-full">
                <div className="w-[48%]">
                  <div className="flex flex-col gap-4">
                    <div className="flex flex-row gap-4">
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
                    </div>
                    <div className="flex flex-row gap-4">
                      <div className="flex flex-col gap-2">
                        <Label htmlFor="name">Имя</Label>
                        <Input type="text" id="name" placeholder="Иван" />
                      </div>
                      <div className="flex flex-col gap-2">
                        <Label htmlFor="policy">Отчество</Label>
                        <Input type="text" id="policy" placeholder="Иванович" />
                      </div>
                    </div>
                    <div className="flex flex-row gap-4">
                      <div className="flex flex-col gap-2">
                        <Label htmlFor="name">Пол</Label>
                        <Select
                          value={selectedGender}
                          onValueChange={(value) => {
                            setSelectedGender(value);
                          }}
                        >
                          <SelectTrigger className="w-[180px]">
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
                  </div>
                </div>
                <Separator orientation="vertical" className="text-gray-900" />
                <div className="w-[48%]">
                  {!selectedFile && (
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
                      <Button
                        variant="outline"
                        className="hover:cursor-pointer"
                      >
                        Отменить
                      </Button>
                    </div>
                  )}
                </div>
              </div>
              <Separator />
              <DialogFooter>
                <Button variant="outline">Отмена</Button>
                <Button>Добавить исследование</Button>
              </DialogFooter>
            </DialogContent>
          </form>
        </Dialog>
        <Dialog>
          <form>
            <DialogTrigger asChild>
              <Button variant="outline">Добавить набор исследований</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Загрузка КТ исследования</DialogTitle>
                <DialogDescription>
                  Добавьте .zip архив одного исследования
                </DialogDescription>
                <Separator className="text-white" />
              </DialogHeader>
              {!selectedFile && (
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
              )}
            </DialogContent>
          </form>
        </Dialog>
        {/* <Input
          placeholder="Сервис"
          
          className="flex w-[300px]"
        /> */}
      </div>
      
      {/* <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Ресурс</TableHead>
            <TableHead>Частота</TableHead>
            <TableHead>Последний пинг</TableHead>
            <TableHead>Статус</TableHead>
            <TableHead />
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow>
            <TableCell className="font-medium">https://i.moscow/</TableCell>
            <TableCell>2 (мин)</TableCell>
            <TableCell>13:50:02 | 21.09.25</TableCell>
            <TableCell>
              <p className="px-2 py-1 rounded-md border border-lime-700 bg-lime-100 text-lime-500 inline-block">
                В работе
              </p>
            </TableCell>
            <TableCell>
              <Link href="/i-moscow">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <ExternalLink height={20} width={20} />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Перейти к отчету</p>
                  </TooltipContent>
                </Tooltip>
              </Link>
            </TableCell>
            <TableCell>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Pen height={20} width={20} />
                </TooltipTrigger>
                <TooltipContent>
                  <p>Редактировать</p>
                </TooltipContent>
              </Tooltip>
            </TableCell>
            <TableCell>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Pause height={20} width={20} />
                </TooltipTrigger>
                <TooltipContent>
                  <p>Приостановить</p>
                </TooltipContent>
              </Tooltip>
            </TableCell>
            <TableCell>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Trash height={20} width={20} className="text-red-700" />
                </TooltipTrigger>
                <TooltipContent>
                  <p>Удалить</p>
                </TooltipContent>
              </Tooltip>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table> */}
    </div>
  );
}
