defmodule Solution do
  def parse_file(filename) do
    File.read!(filename)
    |> String.trim("\n")
    |> String.split("\n")
    |> Enum.chunk_by(fn x -> x != "" end)
    |> Enum.reject(fn x -> x == [""] end)

    # |> dbg
  end

  def register_cols_and_get_length(pid, nrs) do
    nrs
    |> String.replace(" ", "", global: true)
    |> String.graphemes()
    |> Enum.map(fn x ->
      Agent.update(pid, fn map -> Map.put(map, String.to_integer(x), []) end)
      x
    end)
    |> length

    # |> dbg
  end

  def parse_boxes(pid, boxes, cols) do
    boxes
    |> Enum.map(fn row ->
      row
      |> String.pad_trailing(4 * cols, " ")
      |> String.graphemes()
      |> Enum.chunk_every(4)
      |> Enum.reduce(1, fn [_, x, _, _], acc ->
        stack = Agent.get(pid, fn map -> Map.get(map, acc) end)

        case x do
          " " -> :ok
          _ -> Agent.update(pid, fn map -> Map.put(map, acc, [x | stack]) end)
        end

        acc + 1
      end)
    end)

    # |> dbg
  end

  def parse_instr(instr) do
    instr
    |> Enum.map(fn line ->
      line
      |> String.replace(["move ", "from ", "to "], "", global: true)
      |> String.split(" ")
      |> Enum.map(fn x -> String.to_integer(x) end)
    end)

    # |> dbg
  end

  def collect(_pid, acc, stop_idx, stop_idx) do
    acc
  end

  def collect(pid, acc, idx, stop_idx) do
    [top | _] =
      case Agent.get(pid, fn map -> Map.get(map, idx) end) do
        [] -> ["", []]
        [x] -> [x, []]
        x -> x
      end

    collect(pid, top <> acc, idx - 1, stop_idx)
  end

  def ex1(filename) do
    [boxes, instr] = parse_file(filename)

    [nrs | boxes] = boxes |> Enum.reverse()
    # |> dbg

    {:ok, pid} = Agent.start_link(fn -> %{} end)

    cols = register_cols_and_get_length(pid, nrs)

    parse_boxes(pid, boxes, cols)
    steps = parse_instr(instr)

    steps
    |> Enum.map(fn [move, from, to] ->
      Enum.each(1..move, fn _ ->
        to_stack = Agent.get(pid, fn map -> Map.get(map, to) end)
        [popped | from_stack] = Agent.get(pid, fn map -> Map.get(map, from) end)
        Agent.update(pid, fn map -> Map.put(map, from, from_stack) end)
        Agent.update(pid, fn map -> Map.put(map, to, [popped | to_stack]) end)
      end)
    end)

    # |> dbg

    top_of_stacks = collect(pid, "", cols, 0)

    Agent.stop(pid, :normal)

    top_of_stacks
  end

  def ex2(filename) do
    [boxes, instr] = parse_file(filename)

    [nrs | boxes] = boxes |> Enum.reverse()
    # |> dbg

    {:ok, pid} = Agent.start_link(fn -> %{} end)

    cols = register_cols_and_get_length(pid, nrs)

    parse_boxes(pid, boxes, cols)
    steps = parse_instr(instr)

    steps
    |> Enum.map(fn [move, from, to] ->
      to_stack = Agent.get(pid, fn map -> Map.get(map, to) end)
      from_stack = Agent.get(pid, fn map -> Map.get(map, from) end)

      popped = Enum.take(from_stack, move)
      from_stack = Enum.drop(from_stack, move)

      Agent.update(pid, fn map -> Map.put(map, from, from_stack) end)
      Agent.update(pid, fn map -> Map.put(map, to, List.flatten([popped | to_stack])) end)
    end)

    # |> dbg

    top_of_stacks = collect(pid, "", cols, 0)

    Agent.stop(pid, :normal)

    top_of_stacks
  end
end

IO.write("ex1: #{Solution.ex1("input.txt")}\n")
IO.write("ex2: #{Solution.ex2("input.txt")}\n")
