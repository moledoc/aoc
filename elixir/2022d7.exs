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
          Agent.update(pid, fn(map) -> Map.update(map, e, isize, fn(x) -> x+isize end) end)
        end)

        parse(pid, Enum.drop(lines, 1), cur_dir)
       x ->
         throw "unexpected case: '#{x}'"
    end
  end

  def ex1(filename) do
    lines = File.read!(filename)
    |> String.trim("\n")
    |> String.split("\n")

    {:ok, pid} = Agent.start_link(fn -> %{} end)
    parse(pid, lines, "")
    mp = Agent.get(pid, fn(map) -> map end)
    Agent.stop(pid, :normal)

    vs = for {_, v} <- mp, do: v
    vs = Enum.sort(vs)

    IO.inspect(mp)
    Enum.reduce(vs, 0, fn(x, acc) -> acc+x <= 100_000 && acc+x || acc end)
  end

end

IO.write("ex1: #{Solution.ex1("input.txt")}\n")
# too low: 64012

# IO.write("ex2: #{Solution.ex2("tmp.txt")}\n")
