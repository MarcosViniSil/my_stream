import {
  Input,
  InputGroup,
  InputLeftElement,
  Button,
  Box,
  Stack,
  useBreakpointValue,
} from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import { BsToggleOff } from "react-icons/bs";
import { BsToggleOn } from "react-icons/bs";
import { createContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AccessibleContext } from "../../context/AccessibleContext";
import React, { useContext } from 'react';

function SearchBar({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState("");
  const { accessible, toggleAccessible } = useContext(AccessibleContext);
  
 const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) onSearch(searchTerm);
  };


  const stackDirection = useBreakpointValue({ base: "column", md: "row" });

  return (
      <form onSubmit={handleSubmit}>
        <Stack direction={stackDirection} spacing={2} align="stretch">
          <InputGroup width={{ md: "300px" }}>
            <InputLeftElement pointerEvents="none">
              <SearchIcon color="gray.400" />
            </InputLeftElement>
            <Input
              type="text"
              placeholder="Pesquisar"
              aria-label="Caixa de texto para buscar por um título"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              bg="#121212"
              color="white"
              border="1px solid #333"
              borderRadius="full"
              _placeholder={{ color: "gray.500" }}
              _focus={{
                boxShadow: "none",
                borderColor: "#555",
              }}
            />
          </InputGroup>

          <Button
            type="submit"
            aria-label="Botão de pesquisar por um título"
            color="gray.300"
            bg="#121212"
            border="1px solid #333"
            borderRadius="full"
            _hover={{ bg: "#1f1f1f", borderColor: "#555" }}
            _active={{ bg: "#1f1f1f", borderColor: "#555" }}
            _focus={{ boxShadow: "none", borderColor: "#555" }}
            px={4}
          >
            <SearchIcon />
          </Button>
          <Stack direction={stackDirection} align="stretch" spacing={10} color="white" aria-label="Ativar acessibilidade">
            <Button variant="ghost" color="white" onClick={toggleAccessible} gap="5px"  _hover={{ background: "none", boxShadow: "none" }}>
              <p style={{ fontSize: "1.55rem" }}>Acessibilidade</p>  {accessible ? <BsToggleOn size={35} /> : <BsToggleOff size={35} />}
            </Button>
          </Stack>
        </Stack>
      </form>
  );
}

export default SearchBar;
