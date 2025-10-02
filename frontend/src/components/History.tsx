"use client";
import {
  ColumnDef,
  ColumnFiltersState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
  VisibilityState,
} from "@tanstack/react-table";

import { ArrowUpDown, ChevronDown, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { strict } from "assert";
import Link from "next/link";

export type Study = {
  created_at: Date
  id: number
  // markup_file: string
  name: string
  path_to_study: string
  pathology: string
  probability_of_pathology: string
  processing_status: string
  series_uid: number
  study_uid: number
  time_of_processing: any
  // updated_at: Date
  work_ai_status: string
}

const getDate = (date) => {
  const dateTime = date.split(".")[0];
  return dateTime.split("T")[0] + " " + dateTime.split("T")[1];
}

const loadExcel = (id) => {
  const formData = new FormData()
  formData.append('id', id)
  
  fetch(`http://0.0.0.0:8001/api/patient/scans/export/?scan_ids=${id}`, {
    method: "POST"
  })
    .then((res) => res.blob())
    .catch((e) =>
      console.log(e)
    );
}

async function downloadExcel(id) {
      try {
    
       const response = await fetch(`http://0.0.0.0:8001/api/patient/scans/export/?scan_ids=${id}`, {
          method: 'POST'
       });
  
     if (!response.ok) {
       // Если сервер вернул ошибку, обрабатываем ее
        const errorData = await response.json().catch(() => ({ message: 'Не удалось обработать ошибку' }));
        throw new Error(`Ошибка сервера: ${response.status} ${response.statusText}. ${errorData.message}`
      );
      }
   
  
       const blob = await response.blob();
   

     const objectUrl = window.URL.createObjectURL(blob);
   
   
        const link = document.createElement('a');
        link.href = objectUrl;
       document.body.appendChild(link);
       link.click();
   
     
      document.body.removeChild(link);
      window.URL.revokeObjectURL(objectUrl);
  
      } catch (error) {
        console.error('Произошла ошибка при скачивании файла:', error);

      }
    }

export const columns: ColumnDef<Study>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "created_at",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Создано
          <ArrowUpDown />
        </Button>
      );
    },
    cell: ({ row }) => (
      <div className="capitalize">{getDate(row.getValue("created_at"))}</div>
    ),
  },
  {
    accessorKey: "name",
    header: "Название",
    cell: ({ row }) => <div className="capitalize">{row.getValue("name")}</div>,
  },
  {
    accessorKey: "path_to_study",
    header: "Путь к исследованию",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("path_to_study")}</div>
    ),
  },
  {
    accessorKey: "study_uid",
    header: "ID исследования",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("study_uid")}</div>
    ),
  },
  {
    accessorKey: "series_uid",
    header: "ID серии",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("series_uid")}</div>
    ),
  },
  {
    accessorKey: "pathology",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Норма
          <ArrowUpDown />
        </Button>
      );
    },
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("pathology")}</div>
    ),
  },
  {
    accessorKey: "probability_of_pathology",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Вероятность патологии
          <ArrowUpDown />
        </Button>
      );
    },
    cell: ({ row }) => (
      <div className="capitalize">
        {row.getValue("probability_of_pathology")}
      </div>
    ),
  },
  {
    accessorKey: "processing_status",
    header: "Статус проверки",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("processing_status")}</div>
    ),
  },
  {
    accessorKey: "work_ai_status",
    header: "Статус обработки ИИ",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("work_ai_status")}</div>
    ),
  },
  {
    accessorKey: "time_of_processing",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Время обработки (с)
          <ArrowUpDown />
        </Button>
      );
    },
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("time_of_processing")}</div>
    ),
  },
  // {
  //   accessorKey: "email",
  //   header: ({ column }) => {
  //     return (
  //       <Button
  //         variant="ghost"
  //         onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
  //       >
  //         Email
  //         <ArrowUpDown />
  //       </Button>
  //     )
  //   },
  //   cell: ({ row }) => <div className="lowercase">{row.getValue("email")}</div>,
  // },
  // {
  //   accessorKey: "amount",
  //   header: () => <div className="text-right">Amount</div>,
  //   cell: ({ row }) => {
  //     const amount = parseFloat(row.getValue("amount"))
  //     // Format the amount as a dollar amount
  //     const formatted = new Intl.NumberFormat("en-US", {
  //       style: "currency",
  //       currency: "USD",
  //     }).format(amount)
  //     return <div className="text-right font-medium">{formatted}</div>
  //   },
  // },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row }) => {
      const payment = row.original;
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {payment.path_to_study?.length > 0 && (
              <DropdownMenuItem>
                <Link href={payment.path_to_study}>
                  Скачать загруженный архив
                </Link>
              </DropdownMenuItem>
            )}
            <DropdownMenuItem>
              <p onClick={() => downloadExcel(payment.id)}>
                Скачать отчет в .xls
              </p>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  },
];

const History = () => {
  const [researches, setResearches] = useState([]);
  useEffect(() => {
    fetch("http://0.0.0.0:8001/api/patient/scans/", {
      method: "GET",
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.length) {
          setResearches(res);
        }
      })
      .catch((e) => toast.error(`Ошибка загрузки данных: ${e}`, {
        style: {
          backgroundColor: "rgba(193, 0, 7, 0.48)",
          borderColor: "#c10007",
        },
      }))
    }, [])
 
   const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>(
    []
  )
  const [columnVisibility, setColumnVisibility] =
    useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = useState({})
  const table = useReactTable({
    data: researches,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  })
  return <div className="w-full">
      {/* <div className="flex items-center py-4">
        <Input
          placeholder="Filter emails..."
          value={(table.getColumn("email")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("email")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              Columns <ChevronDown />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) =>
                      column.toggleVisibility(!!value)
                    }
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                )
              })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div> */}
      <div className="overflow-hidden rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  )
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  Нет данных.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="text-muted-foreground flex-1 text-sm">
          {table.getFilteredSelectedRowModel().rows.length} из {" "}
          {table.getFilteredRowModel().rows.length} исследований выбрано.
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Назад
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Вперед
          </Button>
        </div>
      </div>
    </div>
  ;
};

export default History;
