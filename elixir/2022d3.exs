defmodule Solution do
  def ex1(filename) do
    contents = File.read!(filename) 
    |> String.trim("\n")
    |> String.split("\n")
    |> Enum.map(fn(x) -> String.split_at(x, floor(String.length(x)/2)) end) 
    # |> dbg

    sum = contents |> Enum.map(fn({a1,a2}) -> 
      {:ok, pid} = Agent.start_link(fn -> %{} end)

      _ = a1 
      |> to_charlist 
      |> Enum.map(fn(char) -> Agent.update(pid, fn(map) -> Map.put(map, char, char) end) end)
      # |> dbg

      line_sum = a2 
      |> to_charlist 
      |> Enum.map(fn(char) -> Agent.get(pid, fn(map) -> Map.get(map, char) end) end)
      |> Enum.uniq
      |> Enum.reduce(0, fn(c, acc) -> 
        case c do
          nil -> acc+0
          _ when c >= ?a -> acc+(c-?a+1)
          _ when c >= ?A -> acc+(c-?A+27)
          _ -> acc+0
        end
      end)
      # |> dbg

      Agent.stop(pid, :normal)
      line_sum
    end)
    |> Enum.sum
    sum
  end

  def ex2(filename) do
    contents = File.read!(filename) 
    |> String.trim("\n")
    |> String.split("\n")
    |> Enum.chunk_every(3)
    # |> dbg

    sum = contents |> Enum.map(fn([a1,a2,a3]) -> 
      {:ok, pid1} = Agent.start_link(fn -> %{} end)
      {:ok, pid2} = Agent.start_link(fn -> %{} end)

      _ = a1 
      |> to_charlist 
      |> Enum.map(fn(char) -> Agent.update(pid1, fn(map) -> Map.put(map, char, char) end) end)
      # |> dbg

      _ = a2 
      |> to_charlist 
      |> Enum.map(fn(char) -> Agent.get(pid1, fn(map) -> Map.get(map, char) end) end)
      |> Enum.uniq
      |> Enum.map(fn(char) -> 
        case char do
          nil -> nil
          _ -> Agent.update(pid2, fn(map) -> Map.put(map, char, char) end) 
        end
      end)

      line_sum = a3 
      |> to_charlist 
      |> Enum.map(fn(char) -> Agent.get(pid2, fn(map) -> Map.get(map, char) end) end)
      |> Enum.uniq
      |> Enum.reduce(0, fn(c, acc) -> 
        case c do
          nil -> acc+0
          _ when c >= ?a -> acc+(c-?a+1)
          _ when c >= ?A -> acc+(c-?A+27)
          _ -> acc+0
        end
      end)
      # |> dbg

      Agent.stop(pid1, :normal)
      Agent.stop(pid2, :normal)
      line_sum
    end)
    |> Enum.sum
    sum
  end
end

IO.write("ex1: #{Solution.ex1("input.txt")}\n")
IO.write("ex2: #{Solution.ex2("input.txt")}\n")
