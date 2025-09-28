"use client";

import * as React from "react";
import { format, parse, isValid } from "date-fns";
import { ru } from "date-fns/locale";
import { Calendar as CalendarIcon } from "lucide-react";
import { DayPickerSingleProps } from "react-day-picker";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Input } from "@/components/ui/input";

export function DatePickerRu() {
  const [date, setDate] = React.useState<Date>();
  const [inputValue, setInputValue] = React.useState<string>("");
  const [month, setMonth] = React.useState<Date>(new Date());

  React.useEffect(() => {
    if (date) {
      setInputValue(format(date, "dd.MM.yyyy", { locale: ru }));
      setMonth(date); // Sync month with selected date
    } else {
      setInputValue("");
    }
  }, [date]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = e.target.value.replace(/[^\d]/g, "");

    if (value.length > 2) {
      value = `${value.slice(0, 2)}.${value.slice(2)}`;
    }
    if (value.length > 5) {
      value = `${value.slice(0, 5)}.${value.slice(5, 9)}`;
    }

    setInputValue(value);

    if (value.length === 10) { // dd.MM.yyyy
      const parsedDate = parse(value, "dd.MM.yyyy", new Date(), { locale: ru });
      if (isValid(parsedDate)) {
        setDate(parsedDate);
        setMonth(parsedDate); // Also update the calendar view to this month
      } else {
        setDate(undefined);
      }
    } else {
      setDate(undefined);
    }
  };

  const handleDateSelect: DayPickerSingleProps['onSelect'] = (selectedDate) => {
    if (selectedDate) {
        setDate(selectedDate);
    }
  };

  return (
    <div className="relative w-[180px]">
      <Input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="дд.мм.гггг"
        className="w-full pr-10 pl-3 text-left font-normal"
        maxLength={10}
      />
      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant={"outline"}
            className={cn(
              "absolute right-0 top-0 h-full rounded-l-none border-l",
              !date && "text-muted-foreground"
            )}
          >
            <CalendarIcon className="h-4 w-4" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0">
          <Calendar
            mode="single"
            selected={date}
            onSelect={handleDateSelect}
            month={month}
            onMonthChange={setMonth}
            initialFocus
            locale={ru}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}