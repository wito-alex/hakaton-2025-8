"use client";

import React, { JSX, ReactHTMLElement } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { ArrowUpDown } from "lucide-react";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { DataTable } from "@/components/ui/data-table";

// 1. Define the data structure for a single row
export type User = {
  id: number;
  name: string;
  email: string;
  role: "Admin" | "User" | "Editor";
  status: "Active" | "Inactive" | "Pending";
  creationDate: string;
  lastLogin: string;
  active?: any
};

// 2. Create the test data
const testData: User[] = [
  {
    id: 1,
    name: "Иван Иванов",
    email: "ivan.ivanov@example.com",
    role: "Admin",
    status: "Active",
    creationDate: "2023-01-15",
    lastLogin: "2024-07-20",
    active: <Button>lalala</Button>
  },
  {
    id: 2,
    name: "Мария Кузнецова",
    email: "maria.kuznetsova@example.com",
    role: "Editor",
    status: "Active",
    creationDate: "2023-02-20",
    lastLogin: "2024-07-19",
  },
  {
    id: 3,
    name: "Петр Сидоров",
    email: "petr.sidorov@example.com",
    role: "User",
    status: "Inactive",
    creationDate: "2023-03-10",
    lastLogin: "2024-01-05",
  },
  {
    id: 4,
    name: "Анна Попова",
    email: "anna.popova@example.com",
    role: "User",
    status: "Pending",
    creationDate: "2024-05-30",
    lastLogin: "2024-07-21",
  },
  {
    id: 5,
    name: "Сергей Смирнов",
    email: "sergey.smirnov@example.com",
    role: "Editor",
    status: "Active",
    creationDate: "2022-11-11",
    lastLogin: "2024-07-21",
  },
];

// 3. Define the columns for the data table with sorting on all columns
export const columns: ColumnDef<User>[] = [
  {
    accessorKey: "id",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        ID
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "name",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        Имя
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "email",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        Email
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "role",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        Роль
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "status",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        Статус
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "creationDate",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        Дата создания
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "lastLogin",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        Последний вход
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
];

export default function Home() {
  const handleRowClick = (row: User) => {
    // Example action on row click
    alert(`Вы кликнули на пользователя: ${row.name}`);
  };

  return (
    <>
      <div className="flex flex-col gap-4 p-4 bg-slate-800/50 rounded-lg">
        <h1 className="text-2xl font-bold">Таблица пользователей</h1>
        <DataTable
          columns={columns}
          data={testData}
          onRowClick={handleRowClick}
        />
      </div>

      <div className="flex flex-col gap-4 mt-10 px-4 py-2 bg-slate-600/30 rounded-md">
        <div className="font-bold uppercase">Панель управления</div>
        <div className="flex flex-row gap-4">
          <div className="flex flex-col gap-2 border rounded-md p-2 bg-slate-500/30">
            <div className="">Частота проверок</div>
            <div className="font-semibold">Каждые 5 минут</div>
          </div>
          <div className="flex flex-col gap-2 border rounded-md p-2 bg-slate-500/30">
            <div className="">Количество попыток</div>
            <div className="font-semibold">2 попытки подключения</div>
          </div>
          <div className="flex flex-col gap-2 border rounded-md p-2 bg-slate-500/30">
            <div className="">Уведомлять о</div>
            <div className="font-semibold">каждой проблеме</div>
          </div>
          <div className="flex flex-col gap-2 border rounded-md p-2 bg-slate-500/30">
            <ul>
              <li className="list-disc ml-3 font-bold">push в системе</li>
              <li className="list-disc ml-3 font-bold">tg:@silichium</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-4 mt-10 px-4 py-2 bg-slate-600/30 rounded-md">
        <div className="grid grid-cols-3 gap-3">
          <div className="flex-col gap-4 border rounded-md p-4">
            <p>Количество сбоев за неделю</p>
            <p>График</p>
            <p className="font-bold">1 сбой на 70 проверок</p>
          </div>
          <div className="flex-col gap-4 border rounded-md p-4">
            <p>Успешно с первой попытки</p>
            <p>График</p>
            <p className="font-bold">99%</p>
          </div>
          <div className="flex-col gap-4 border rounded-md p-4">
            <p>Еще одна метрика</p>
            <p>График</p>
            <p className="font-bold">99%</p>
          </div>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Ресурс</TableHead>
              <TableHead>Время ответа</TableHead>
              <TableHead>Время пинга</TableHead>
              <TableHead>Статус</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell className="font-medium">https://i.moscow/</TableCell>
              <TableCell>10 сек</TableCell>
              <TableCell>13:50:02</TableCell>
              <TableCell>Успешно</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </>
  );
}