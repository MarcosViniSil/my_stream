import {
  Input,
  InputGroup,
  InputLeftElement,
  Button,
  Stack,
  useBreakpointValue,
} from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import { useState } from "react";

function SearchBar({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSearchClick = () => {
    if (onSearch) onSearch(searchTerm);
  };

  const stackDirection = useBreakpointValue({ base: "column", md: "row" });

  return (
    <Stack direction={stackDirection} spacing={2} width="50%">
      <InputGroup width={{ base: "100%", md: "300px" }}>
        <InputLeftElement pointerEvents="none">
          <SearchIcon color="gray.500" />
        </InputLeftElement>
        <Input
          type="text"
          placeholder="Buscar..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          bg="white"
          color="black"
          border="none"
          _focus={{ boxShadow: "none", border: "none" }}
        />
      </InputGroup>
      <Button
        className="buttonSendSearch"
        onClick={handleSearchClick}
        width={{ base: "100%", md: "auto" }}
      >
        Pesquisar
      </Button>
    </Stack>
  );
}

export default SearchBar;
