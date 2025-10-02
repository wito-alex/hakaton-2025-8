"use client"
import { LogOut, Moon, Sun, Settings, User, BookOpenCheck } from "lucide-react";
import Link from 'next/link'
import {useState} from 'react'
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { hasCookie, setCookie, deleteCookie } from "cookies-next";
import { useRouter } from "next/router";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";
import { motion } from "framer-motion";
import Logo from "../assets/lungs.png";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const Navbar = () => {
  const [isDark, setIsDark] = useState(true)
  const { setTheme } = useTheme();


  const changeTheme = () => {
    setIsDark((prevState) => !prevState);
    !isDark ? setTheme("dark") : setTheme("light")
  }

    const logOut = () => {
      deleteCookie('refresh');
    };

  return (
    <nav className="p-4 flex items-center justify-between">
      <Link href="/" className="flex items-center gap-2">
        <figure className="">
          <motion.img src={Logo.src} alt="logo" className="h-8" />
        </figure>
        <div className="flex flex-row items-center">
          <p className="text-lg">RESPIRATIO</p>
        </div>
      </Link>
      <div className="flex flex-row gap-2">
        <Link href="/" className="flex items-center gap-2">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button variant="outline" size="icon" onClick={logOut}>
                <BookOpenCheck
                  className={`h-[1.2rem] w-[1.2rem] text-lime-300`}
                />
              </Button>
            </TooltipTrigger>
            <TooltipContent>
              <p>Руководство</p>
            </TooltipContent>
          </Tooltip>
        </Link>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="outline" size="icon" onClick={changeTheme}>
              <Sun
                className={`h-[1.2rem] w-[1.2rem]  text-yellow-500 ${
                  isDark ? "hidden" : "flex"
                }`}
              />
              <Moon
                className={`h-[1.2rem] w-[1.2rem]  text-yellow-300 ${
                  isDark ? "flex" : "hidden"
                }`}
              />
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            {isDark ? <p>Светлый режим</p> : <p>Темный режим</p>}
          </TooltipContent>
        </Tooltip>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="outline" size="icon" onClick={logOut}>
              <LogOut className={`h-[1.2rem] w-[1.2rem] text-cyan-300`} />
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Выйти</p>
          </TooltipContent>
        </Tooltip>
      </div>
    </nav>
  );
}

export default Navbar