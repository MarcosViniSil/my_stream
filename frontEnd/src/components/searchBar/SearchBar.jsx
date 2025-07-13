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

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) onSearch(searchTerm);
  };

  const stackDirection = useBreakpointValue({ base: "row", md: "row" });

  return (
    <form onSubmit={handleSubmit}>
      <Stack direction={stackDirection} spacing={2}>
        <InputGroup width={{ md: "300px" }}>
          <InputLeftElement pointerEvents="none">
            <SearchIcon color="gray.400" />
          </InputLeftElement>
          <Input
            type="text"
            placeholder="Pesquisar"
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
      </Stack>
    </form>
  );
}

export default SearchBar;
