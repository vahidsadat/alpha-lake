"use client";
import { useEffect, useState } from "react";
import styled from "@emotion/styled";
import CssBaseline from '@mui/material/CssBaseline';
import Button from '@mui/material/Button';
import SearchIcon from '@mui/icons-material/Search';
const Input = styled.input`
    width: 100%;
    padding: 0.2rem;
    font-size: large;
`;
interface SearchBarProps {
    searchTerm: string;
    onSearchTermChange: (newSearchTerm: string) => void;
}

const SearchBar = ({ searchTerm, onSearchTermChange }: SearchBarProps) => {
    return (
        <div className= "flex flex-rows gap-2 items-center">
            <div className= "w-full">
                <Input
                    type="text"
                    placeholder="search company..."
                    className="w-full p-2 border border-gray-300 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500"
                    value={searchTerm}
                    onChange={(e) => onSearchTermChange(e.target.value)}
                    />
            </div>
            <Button variant="contained" href="#contained-buttons">
                <SearchIcon />
            </Button>
        </div>
    );
}
export default SearchBar;