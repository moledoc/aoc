defmodule Solution do

  def parse(pid, lines, cur_dir) do
    elems = List.first(lines, "")
    |> String.split(" ")

    case elems do
      [""] -> :ok
      ["$", "cd", "/"] -> 
        parse(pid, Enum.drop(lines, 1), "/")
      ["$", "cd", ".."] -> 
        parse(pid, Enum.drop(lines, 1), Path.dirname(cur_dir))
        :ok
      ["$", "cd", x] -> parse(pid, Enum.drop(lines, 1), Path.absname(cur_dir <> "/" <> x))
      ["dir", _x] -> parse(pid, Enum.drop(lines, 1), cur_dir)
      ["$", "ls"] -> parse(pid, Enum.drop(lines, 1), cur_dir)
      [size, _file] -> 
        isize = String.to_integer(size)

	es = String.split(cur_dir, "/") 

        es_len = case es do
          ["", ""] -> 1
          _ -> length(es)
        end

        Enum.each(1..es_len, fn(x) ->
          e = es 
          |> Enum.take(x) 
          |> Enum.join("/")

          e = Path.absname("/" <> e)
          IO.inspect(es)
          IO.inspect(cur_dir)
          Agent.update(pid, fn(map) -> Map.update(map, e, isize, fn(x) -> x+isize end) end)
        end)

        parse(pid, Enum.drop(lines, 1), cur_dir)
       x ->
         IO.inspect("unexpected case: #{x}\n")
    end
  end

  def ex1(filename) do
    lines = File.read!(filename)
    |> String.trim("\n")
    |> String.split("\n")

    {:ok, pid} = Agent.start_link(fn -> %{} end)
    parse(pid, lines, "")
    IO.inspect(Agent.get(pid, fn(map) -> map end))
    Agent.stop(pid, :normal)
  end

end

IO.inspect("ex1: #{Solution.ex1("tmp.txt")}\n")
# IO.write("ex2: #{Solution.ex2("tmp.txt")}\n")

# Map.update(%{a: 1}, :a, 13, fn existing_value -> existing_value * 2 end)
    # %{a: 2}
# Map.update(a, "/", 0, fn(x) -> x+1 end)
